new_func = r'''    async function parseAndRenderAIResponse(text, targetEl) {
      // Step 1: [DERIVED:] tags first
      const derivedQueue = [];
      let processedText = text.replace(/\[DERIVED:\s*([^\]=]+?)\s*=\s*([^\]]+)\]/gi, (_, varName, formula) => {
        const name = varName.trim();
        const chipId = `derived-chip-${name.replace(/\W/g, '_')}`;
        derivedQueue.push({ name, formula: formula.trim(), chipId });
        return `<span id="${chipId}" class="derived-chip derived-chip--pending">Creating: ${name}</span>`;
      });

      // Step 2: Parse all chart tags + Markdown into HTML
      let plotCounter = 0;
      const plotQueue = [];

      const makeExportConfig = (label) => ({
        responsive: true, displaylogo: false,
        modeBarButtonsToRemove: ['toImage'],
        modeBarButtonsToAdd: [
          { name: 'PNG (white)', title: 'Save PNG (white bg)', icon: Plotly.Icons.camera, click: (gd) => downloadImageWithBg(gd, label, '#ffffff', '#333333') },
          { name: 'PNG (dark)',  title: 'Save PNG (dark bg)',  icon: Plotly.Icons.camera, click: (gd) => downloadImageWithBg(gd, label, '#0f172a', '#e2e8f0') },
          { name: 'HTML', title: 'Export as standalone HTML', icon: { width:1024, height:1024, path:'M256,128 L768,128 L768,896 L256,896 Z M384,320 L640,320 M384,512 L640,512 M384,704 L512,704' }, click: (gd) => exportPlotHTML(gd, label) }
        ]
      });

      // Helper: fetch plot data with smart fallback on 400
      // Returns { data } on success, or { error, missing } on failure
      async function fetchPlotData(xVar, yVarList, maxPoints) {
        const fd = new FormData();
        fd.append('x_var', xVar);
        yVarList.forEach(v => fd.append('y_vars', v));
        fd.append('max_points', String(maxPoints || 2000));
        const r = await fetch(`${API}/plot-data`, { method: 'POST', body: fd });
        if (r.ok) {
          const d = await r.json();
          return { data: d.data || {} };
        }
        let msg = `HTTP ${r.status}`;
        try { const j = await r.json(); msg = j.message || msg; } catch(_) {}
        // Parse missing column names from message like "Columns not found: ['SFC', 'Total_Fuel_Flow']"
        const missingMatch = msg.match(/\[([^\]]+)\]/);
        const missing = missingMatch ? missingMatch[1].split(',').map(s => s.replace(/['"]/g,'').trim()) : [];
        return { error: msg, missing };
      }

      // Show an error banner inside the plot element
      function showPlotError(el, msg, missingVars) {
        const hint = missingVars && missingVars.length
          ? `<br><small style="color:#94a3b8">Missing column(s): <code>${missingVars.join(', ')}</code>. Run a [DERIVED:] tag or check variable names.</small>`
          : '';
        el.innerHTML = `<p style="color:#f59e0b;padding:10px;font-size:11px">⚠️ ${msg}${hint}</p>`;
      }

      let html = processedText
        .replace(/&/g, '&amp;')

        // [DUALPLOT: Var1,Var2 | Var3,Var4]
        .replace(/\[DUALPLOT:\s*([^\|\]]+)\|\s*([^\]]+)\]/gi, (_, left, right) => {
          const id = `ai-plot-${plotCounter++}`;
          const leftVars  = left.split(',').map(v => v.trim()).filter(Boolean);
          const rightVars = right.split(',').map(v => v.trim()).filter(Boolean);
          plotQueue.push({ id, type: 'dual', leftVars, rightVars, vars: [...leftVars, ...rightVars] });
          return `<div class="ai-plot-block"><div class="ai-plot-title">DUAL Y-AXIS: ${leftVars.join(', ')} | ${rightVars.join(', ')}</div><div id="${id}" style="height:300px;"></div></div>`;
        })

        // [PARALLEL: Var1,...,VarN | COLOR: VarName]
        .replace(/\[PARALLEL:\s*([^\|\]]+)\|\s*COLOR:\s*([^\]]+)\]/gi, (_, vars, colorVar) => {
          const id = `ai-plot-${plotCounter++}`;
          const varList = vars.split(',').map(v => v.trim()).filter(Boolean);
          const cv = colorVar.trim();
          plotQueue.push({ id, type: 'parallel', vars: varList, colorVar: cv });
          return `<div class="ai-plot-block"><div class="ai-plot-title">PARALLEL COORDINATES - Color: ${cv}</div><div id="${id}" style="height:420px;"></div></div>`;
        })

        // [SCATTER: X=Var | Y=Var1,Var2 | COLOR=Var | SCALE=Jet]
        .replace(/\[SCATTER:\s*X=([^\|\]]+)\|\s*Y=([^\|\]]+)(?:\|\s*COLOR=([^\|\]]+))?(?:\|\s*SCALE=([^\]]+))?\]/gi, (_, xv, yv, cv, sc) => {
          const id = `ai-plot-${plotCounter++}`;
          const xVar = xv.trim();
          const yVars = yv.split(',').map(v => v.trim()).filter(Boolean);
          const colorVar = cv ? cv.trim() : null;
          const scale = sc ? sc.trim() : 'Jet';
          const allVars = [...new Set([...yVars, ...(colorVar ? [colorVar] : [])])];
          plotQueue.push({ id, type: 'scatter', xVar, yVars, colorVar, scale, vars: allVars });
          const title = `SCATTER: ${yVars[0]} vs ${xVar}${colorVar ? ' | Color: '+colorVar : ''}`;
          return `<div class="ai-plot-block"><div class="ai-plot-title">${title}</div><div id="${id}" style="height:340px;"></div></div>`;
        })

        // [SCATTER3D: X=Var | Y=Var | Z=Var | COLOR=Var | SCALE=Jet]
        .replace(/\[SCATTER3D:\s*X=([^\|\]]+)\|\s*Y=([^\|\]]+)\|\s*Z=([^\|\]]+)(?:\|\s*COLOR=([^\|\]]+))?(?:\|\s*SCALE=([^\]]+))?\]/gi, (_, xv, yv, zv, cv, sc) => {
          const id = `ai-plot-${plotCounter++}`;
          const xVar = xv.trim(), yVar = yv.trim(), zVar = zv.trim();
          const colorVar = cv ? cv.trim() : null;
          const scale = sc ? sc.trim() : 'Jet';
          const allVars = [...new Set([yVar, zVar, ...(colorVar ? [colorVar] : [])])];
          plotQueue.push({ id, type: 'scatter3d', xVar, yVar, zVar, colorVar, scale, vars: allVars });
          return `<div class="ai-plot-block"><div class="ai-plot-title">3D SCATTER: ${xVar} / ${yVar} / ${zVar}${colorVar ? ' | Color: '+colorVar : ''}</div><div id="${id}" style="height:440px;"></div></div>`;
        })

        // [HISTOGRAM: Var1, Var2, Var3]
        .replace(/\[HISTOGRAM:\s*([^\]]+)\]/gi, (_, vars) => {
          const id = `ai-plot-${plotCounter++}`;
          const varList = vars.split(',').map(v => v.trim()).filter(Boolean);
          plotQueue.push({ id, type: 'histogram', vars: varList });
          return `<div class="ai-plot-block"><div class="ai-plot-title">DISTRIBUTION: ${varList.join(', ')}</div><div id="${id}" style="height:280px;"></div></div>`;
        })

        // [BOX: Var1, Var2, Var3]
        .replace(/\[BOX:\s*([^\]]+)\]/gi, (_, vars) => {
          const id = `ai-plot-${plotCounter++}`;
          const varList = vars.split(',').map(v => v.trim()).filter(Boolean);
          plotQueue.push({ id, type: 'box', vars: varList });
          return `<div class="ai-plot-block"><div class="ai-plot-title">BOX PLOT: ${varList.join(', ')}</div><div id="${id}" style="height:300px;"></div></div>`;
        })

        // [PLOT: Var1, Var2] - standard timeseries (must come AFTER all special tags)
        .replace(/\[PLOT:\s*([^\]]+)\]/gi, (_, vars) => {
          const id = `ai-plot-${plotCounter++}`;
          plotQueue.push({ id, type: 'timeseries', vars: vars.split(',').map(v => v.trim()) });
          return `<div class="ai-plot-block"><div class="ai-plot-title">${vars.trim()}</div><div id="${id}" style="height:260px;"></div></div>`;
        })

        // Markdown
        .replace(/^### (.+)$/gm, '<h3>$1</h3>')
        .replace(/^## (.+)$/gm,  '<h2>$1</h2>')
        .replace(/^# (.+)$/gm,   '<h1>$1</h1>')
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.+?)\*/g,     '<em>$1</em>')
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        .replace(/^(\|.+\|)\r?\n(\|[-| :]+\|)\r?\n((\|.+\|\r?\n?)+)/gm, (_, hdr, sep, body) => {
          const th = hdr.split('|').filter(c=>c.trim()).map(c=>`<th>${c.trim()}</th>`).join('');
          const rows = body.trim().split('\n').map(r => {
            const cells = r.split('|').filter(c=>c.trim()).map(c=>`<td>${c.trim()}</td>`).join('');
            return `<tr>${cells}</tr>`;
          }).join('');
          return `<table><thead><tr>${th}</tr></thead><tbody>${rows}</tbody></table>`;
        })
        .replace(/^[-*] (.+)$/gm, '<li>$1</li>')
        .replace(/(<li>.*<\/li>\n?)+/g, m => `<ul>${m}</ul>`)
        .replace(/^\d+\. (.+)$/gm, '<li>$1</li>')
        .replace(/\n{2,}/g, '</p><p>')
        .replace(/\n/g, '<br>');

      targetEl.innerHTML = `<p>${html}</p>`;

      // Step 3: Create derived variables
      for (const { name, formula, chipId } of derivedQueue) {
        const chip = document.getElementById(chipId);
        try {
          const fd = new FormData();
          fd.append('name', name);
          fd.append('formula', formula);
          const r = await fetch(`${API}/add-derived`, { method: 'POST', body: fd });
          const j = await r.json();
          if (!r.ok) throw new Error(j.message || r.statusText);
          if (j.columns) { columns = j.columns; populateSelectors(); }
          if (chip) chip.outerHTML = `<span class="derived-chip derived-chip--ok">Created: <strong>${name}</strong> = <code>${formula}</code></span>`;
        } catch(err) {
          if (chip) chip.outerHTML = `<span class="derived-chip derived-chip--err">Failed: <strong>${name}</strong> - ${err.message}</span>`;
        }
      }

      // Step 4: Pre-fetch stats once
      let _aiStatsMap = {};
      try {
        const sr = await fetch(`${API}/stats`);
        if (sr.ok) { const sd = await sr.json(); (sd.stats || []).forEach(s => { _aiStatsMap[s.variable] = s; }); }
      } catch(_) {}

      const makeBands = (varName, yref) => {
        yref = yref || 'y';
        const s = _aiStatsMap[varName];
        if (!s || s.q1 == null || s.q3 == null) return [];
        const sh = [{ type:'rect', xref:'paper', yref:yref, x0:0, x1:1, y0:s.q1, y1:s.q3, fillcolor:'rgba(148,163,184,0.12)', line:{width:0}, layer:'below' }];
        if (s.median != null) {
          const iqr = s.q3 - s.q1;
          sh.push({ type:'rect', xref:'paper', yref:yref, x0:0, x1:1, y0:s.median-0.5*iqr, y1:s.median+0.5*iqr, fillcolor:'rgba(34,197,94,0.18)', line:{width:0}, layer:'below' });
        }
        return sh;
      };

      const CHART_COLORS = ['#06b6d4','#a855f7','#22c55e','#f59e0b','#ef4444','#8b5cf6','#14b8a6','#f97316'];

      // Step 5: Render each chart by type
      for (const item of plotQueue) {
        const plotEl = document.getElementById(item.id);
        if (!plotEl) continue;
        const cfg = makeExportConfig(item.vars ? item.vars.join('_') : item.id);

        try {

          // ── TIMESERIES ───────────────────────────────────────────────────
          if (!item.type || item.type === 'timeseries') {
            const result = await fetchPlotData('timestamp', item.vars, 2000);
            if (result.error) { showPlotError(plotEl, result.error, result.missing); continue; }
            const data = result.data;
            const xVals = data['timestamp'] || [];
            const traces = item.vars.filter(v => data[v]).map((v,i) => ({
              x:xVals, y:data[v], name:v, type:'scatter', mode:'lines', line:{width:1.5, color:CHART_COLORS[i%8]}
            }));
            if (!traces.length) { showPlotError(plotEl, 'No data returned for these variables', item.vars); continue; }
            const shapes = [];
            for (const v of item.vars) { const b = makeBands(v); if (b.length) { shapes.push(...b); break; } }
            Plotly.newPlot(plotEl, traces, {
              margin:{t:28,r:10,b:36,l:56}, paper_bgcolor:'rgba(15,23,42,0)', plot_bgcolor:'rgba(15,23,42,0)',
              font:{color:'#94a3b8',size:10}, xaxis:{gridcolor:'rgba(255,255,255,0.07)',color:'#64748b'},
              yaxis:{gridcolor:'rgba(255,255,255,0.07)',color:'#64748b'},
              legend:{font:{size:9},orientation:'h',y:-0.18}, showlegend:traces.length>1, shapes
            }, cfg);
          }

          // ── DUAL Y-AXIS ──────────────────────────────────────────────────
          else if (item.type === 'dual') {
            let { leftVars, rightVars } = item;
            let result = await fetchPlotData('timestamp', [...leftVars, ...rightVars], 2000);

            // Fallback: remove missing vars and retry
            if (result.error && result.missing.length) {
              const allMissing = new Set(result.missing);
              leftVars  = leftVars.filter(v => !allMissing.has(v));
              rightVars = rightVars.filter(v => !allMissing.has(v));
              if (!leftVars.length && !rightVars.length) {
                showPlotError(plotEl, result.error, result.missing); continue;
              }
              result = await fetchPlotData('timestamp', [...leftVars, ...rightVars], 2000);
            }
            if (result.error) { showPlotError(plotEl, result.error, result.missing); continue; }
            const data = result.data;
            const xVals = data['timestamp'] || [];
            const c1 = ['#06b6d4','#a855f7','#22c55e'];
            const c2 = ['#f59e0b','#ef4444','#8b5cf6'];
            const traces = [
              ...leftVars.filter(v=>data[v]).map((v,i) => ({ x:xVals, y:data[v], name:v, type:'scatter', mode:'lines', line:{width:1.8,color:c1[i%3]}, yaxis:'y' })),
              ...rightVars.filter(v=>data[v]).map((v,i) => ({ x:xVals, y:data[v], name:v, type:'scatter', mode:'lines', line:{width:1.8,color:c2[i%3],dash:'dot'}, yaxis:'y2' }))
            ];
            if (!traces.length) { showPlotError(plotEl, 'No data for these variables', [...leftVars,...rightVars]); continue; }
            const shapes = makeBands(leftVars[0] || '', 'y');
            const lLabel = leftVars.join(', ') || '—';
            const rLabel = rightVars.join(', ') || '—';
            Plotly.newPlot(plotEl, traces, {
              margin:{t:28,r:70,b:36,l:60}, paper_bgcolor:'rgba(15,23,42,0)', plot_bgcolor:'rgba(15,23,42,0)',
              font:{color:'#94a3b8',size:10}, xaxis:{gridcolor:'rgba(255,255,255,0.07)',color:'#64748b'},
              yaxis:{title:lLabel, gridcolor:'rgba(255,255,255,0.07)', color:'#06b6d4', titlefont:{color:'#06b6d4',size:10}},
              yaxis2:{title:rLabel, overlaying:'y', side:'right', color:'#f59e0b', titlefont:{color:'#f59e0b',size:10}},
              legend:{font:{size:9},orientation:'h',y:-0.18}, shapes
            }, cfg);
          }

          // ── PARALLEL COORDINATES ─────────────────────────────────────────
          else if (item.type === 'parallel') {
            const { vars: pvars, colorVar } = item;
            const allFetch = [...new Set([...pvars, colorVar])];
            const result = await fetchPlotData('timestamp', allFetch, 5000);
            if (result.error && result.missing.length) {
              // Try without missing vars
              const good = allFetch.filter(v => !result.missing.includes(v));
              if (good.length < 3) { showPlotError(plotEl, result.error, result.missing); continue; }
            }
            if (result.error) { showPlotError(plotEl, result.error, result.missing); continue; }
            const data = result.data;
            const dimensions = pvars.filter(v => data[v]).map(v => {
              const s = _aiStatsMap[v];
              const dim = { label: v.replace(/_/g,' '), values: data[v] };
              if (s && s.min != null && s.max != null) dim.range = [s.min, s.max];
              return dim;
            });
            Plotly.newPlot(plotEl, [{
              type: 'parcoords',
              line: { color: data[colorVar] || [], colorscale: 'Jet', showscale: true,
                colorbar: { title: colorVar.replace(/_/g,' '), titleside:'right', thickness:14, len:0.75, tickfont:{size:9,color:'#94a3b8'}, titlefont:{size:10,color:'#a78bfa'} }
              },
              dimensions, labelangle: -25,
              labelfont: { color: '#cbd5e1', size: 9 }
            }], {
              margin:{t:50,r:90,b:20,l:50}, paper_bgcolor:'rgba(15,23,42,0)', font:{color:'#94a3b8',size:9}
            }, { responsive:true, displaylogo:false });
          }

          // ── SCATTER 2D (X vs Y, optional color + colorscale) ─────────────
          else if (item.type === 'scatter') {
            let { xVar, yVars, colorVar, scale } = item;
            // First try with all vars
            let result = await fetchPlotData(xVar, item.vars, 3000);

            // Smart fallback: if colorVar is missing, retry without it
            if (result.error && result.missing.length && colorVar && result.missing.includes(colorVar)) {
              const varsWithoutColor = item.vars.filter(v => v !== colorVar);
              result = await fetchPlotData(xVar, varsWithoutColor, 3000);
              if (!result.error) colorVar = null; // succeeded without color
            }
            if (result.error) { showPlotError(plotEl, result.error, result.missing); continue; }
            const data = result.data;
            const xVals = data[xVar] || [];
            const colorVals = colorVar ? (data[colorVar] || null) : null;
            const traces = yVars.filter(v => data[v]).map((v, i) => {
              const t = { x:xVals, y:data[v], name:v.replace(/_/g,' '), type:'scatter', mode:'markers',
                marker:{ size:4, opacity:0.65, color: colorVals && i===0 ? colorVals : CHART_COLORS[i%8] }
              };
              if (colorVals && i===0) {
                t.marker.colorscale = scale || 'Jet';
                t.marker.showscale = true;
                t.marker.colorbar = { title: colorVar.replace(/_/g,' '), titleside:'right', thickness:12, len:0.75, tickfont:{size:9,color:'#94a3b8'}, titlefont:{size:10,color:'#a78bfa'} };
              }
              return t;
            });
            if (!traces.length) { showPlotError(plotEl, 'No data for these variables', item.vars); continue; }
            Plotly.newPlot(plotEl, traces, {
              margin:{t:28,r:colorVals?90:20,b:50,l:60}, paper_bgcolor:'rgba(15,23,42,0)', plot_bgcolor:'rgba(15,23,42,0)',
              font:{color:'#94a3b8',size:10},
              xaxis:{title:xVar.replace(/_/g,' '), gridcolor:'rgba(255,255,255,0.07)',color:'#64748b'},
              yaxis:{title:yVars.join(', ').replace(/_/g,' '), gridcolor:'rgba(255,255,255,0.07)',color:'#64748b'},
              legend:{font:{size:9}}
            }, cfg);
          }

          // ── SCATTER 3D ───────────────────────────────────────────────────
          else if (item.type === 'scatter3d') {
            let { xVar, yVar, zVar, colorVar, scale } = item;
            let result = await fetchPlotData(xVar, item.vars, 3000);
            // Fallback: drop colorVar if missing
            if (result.error && result.missing.length && colorVar && result.missing.includes(colorVar)) {
              const varsNoColor = item.vars.filter(v => v !== colorVar);
              result = await fetchPlotData(xVar, varsNoColor, 3000);
              if (!result.error) colorVar = null;
            }
            if (result.error) { showPlotError(plotEl, result.error, result.missing); continue; }
            const data = result.data;
            const colorVals = colorVar ? (data[colorVar] || data[zVar]) : data[zVar];
            Plotly.newPlot(plotEl, [{
              type:'scatter3d', mode:'markers',
              x: data[xVar]||[], y: data[yVar]||[], z: data[zVar]||[],
              marker:{ size:3, color:colorVals, colorscale:scale||'Jet', opacity:0.7, showscale:true,
                colorbar:{ title:(colorVar||zVar).replace(/_/g,' '), titleside:'right', thickness:12, len:0.6, tickfont:{size:8,color:'#94a3b8'} }
              }
            }], {
              margin:{t:20,r:20,b:20,l:20}, paper_bgcolor:'rgba(15,23,42,0)',
              scene:{
                bgcolor:'rgba(15,23,42,0)',
                xaxis:{title:xVar.replace(/_/g,' '), gridcolor:'#1e293b', color:'#64748b'},
                yaxis:{title:yVar.replace(/_/g,' '), gridcolor:'#1e293b', color:'#64748b'},
                zaxis:{title:zVar.replace(/_/g,' '), gridcolor:'#1e293b', color:'#64748b'}
              },
              font:{color:'#94a3b8',size:9}
            }, {responsive:true, displaylogo:false});
          }

          // ── HISTOGRAM ────────────────────────────────────────────────────
          else if (item.type === 'histogram') {
            const result = await fetchPlotData('timestamp', item.vars, 5000);
            if (result.error && result.missing.length) {
              const goodVars = item.vars.filter(v => !result.missing.includes(v));
              if (!goodVars.length) { showPlotError(plotEl, result.error, result.missing); continue; }
              const r2 = await fetchPlotData('timestamp', goodVars, 5000);
              if (r2.error) { showPlotError(plotEl, r2.error, r2.missing); continue; }
              const data = r2.data;
              const traces = goodVars.filter(v => data[v]).map((v, i) => ({
                x:data[v], name:v.replace(/_/g,' '), type:'histogram', opacity:0.72, marker:{color:CHART_COLORS[i%8]}
              }));
              Plotly.newPlot(plotEl, traces, {
                barmode:'overlay', margin:{t:28,r:10,b:50,l:56}, paper_bgcolor:'rgba(15,23,42,0)', plot_bgcolor:'rgba(15,23,42,0)',
                font:{color:'#94a3b8',size:10}, xaxis:{gridcolor:'rgba(255,255,255,0.07)',color:'#64748b'},
                yaxis:{title:'Count', gridcolor:'rgba(255,255,255,0.07)',color:'#64748b'}, legend:{font:{size:9}}
              }, cfg);
              continue;
            }
            if (result.error) { showPlotError(plotEl, result.error, result.missing); continue; }
            const data = result.data;
            const traces = item.vars.filter(v => data[v]).map((v, i) => ({
              x:data[v], name:v.replace(/_/g,' '), type:'histogram', opacity:0.72, marker:{color:CHART_COLORS[i%8]}
            }));
            Plotly.newPlot(plotEl, traces, {
              barmode:'overlay', margin:{t:28,r:10,b:50,l:56}, paper_bgcolor:'rgba(15,23,42,0)', plot_bgcolor:'rgba(15,23,42,0)',
              font:{color:'#94a3b8',size:10}, xaxis:{gridcolor:'rgba(255,255,255,0.07)',color:'#64748b'},
              yaxis:{title:'Count', gridcolor:'rgba(255,255,255,0.07)',color:'#64748b'}, legend:{font:{size:9}}
            }, cfg);
          }

          // ── BOX PLOT ─────────────────────────────────────────────────────
          else if (item.type === 'box') {
            let result = await fetchPlotData('timestamp', item.vars, 5000);
            // Drop missing vars and retry
            if (result.error && result.missing.length) {
              const goodVars = item.vars.filter(v => !result.missing.includes(v));
              if (!goodVars.length) { showPlotError(plotEl, result.error, result.missing); continue; }
              result = await fetchPlotData('timestamp', goodVars, 5000);
            }
            if (result.error) { showPlotError(plotEl, result.error, result.missing); continue; }
            const data = result.data;
            const traces = item.vars.filter(v => data[v]).map((v, i) => ({
              y:data[v], name:v.replace(/_/g,' '), type:'box',
              marker:{color:CHART_COLORS[i%8], size:3},
              boxpoints:'outliers', jitter:0.3, line:{width:1.5}
            }));
            Plotly.newPlot(plotEl, traces, {
              margin:{t:28,r:10,b:65,l:56}, paper_bgcolor:'rgba(15,23,42,0)', plot_bgcolor:'rgba(15,23,42,0)',
              font:{color:'#94a3b8',size:10},
              xaxis:{gridcolor:'rgba(255,255,255,0.07)',color:'#64748b',tickangle:-30},
              yaxis:{gridcolor:'rgba(255,255,255,0.07)',color:'#64748b'},
              legend:{font:{size:9}}
            }, cfg);
          }

        } catch(err) {
          if (plotEl) plotEl.innerHTML = `<p style="color:#f59e0b;padding:8px">Chart error: ${err.message}</p>`;
        }
      }
    }

'''

with open('frontend/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = '    async function parseAndRenderAIResponse(text, targetEl) {'
end_marker = '    function copyAIResponse() {'

start_idx = content.index(start_marker)
end_idx = content.index(end_marker)

new_content = content[:start_idx] + new_func + content[end_idx:]

with open('frontend/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Done. Replaced {end_idx - start_idx} bytes with {len(new_func)} bytes. New total: {len(new_content)} bytes.")
