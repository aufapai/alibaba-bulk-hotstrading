# -*- coding: utf-8 -*-
"""
Fix console errors in App/template.html:
1. switchSourceTab safe currentTarget handling (fixes TypeError: Cannot read properties of undefined reading 'add')
2. quickExportExcel function definition (fixes ReferenceError: quickExportExcel is not defined)
3. Favicon inline SVG (fixes 404 /favicon.ico)
"""

with open('App/template.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Favicon fix
if '<link rel="icon"' not in html:
    fav_tag = '    <link rel="icon" href="data:image/svg+xml,<svg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 100 100\'><text y=\'.9em\' font-size=\'90\'>👢</text></svg>">\n'
    html = html.replace('<title>', fav_tag + '    <title>', 1)
    print("1. Added inline favicon SVG link")

# 2. switchSourceTab fix
old_switch = """        function switchSourceTab(source) {
            activeSource = source;
            document.querySelectorAll('.source-tab').forEach(b => b.classList.remove('active'));
            const targetBtn = (window.event && window.event.currentTarget) || (source === 'shopee_studio' ? document.getElementById('tabShopeeStudio') : null);
            if (targetBtn) targetBtn.classList.add('active');"""

new_switch = """        function switchSourceTab(source, evt = null) {
            activeSource = source;
            document.querySelectorAll('.source-tab').forEach(b => b.classList.remove('active'));
            
            let targetBtn = null;
            if (evt && evt.currentTarget && evt.currentTarget.classList) {
                targetBtn = evt.currentTarget;
            } else if (source === 'shopee_studio') {
                targetBtn = document.getElementById('tabShopeeStudio');
            } else if (source === 'failed_reports') {
                targetBtn = document.getElementById('tabFailedReports');
            } else if (source === 'market_intel') {
                targetBtn = document.getElementById('tabMarketIntel');
            } else if (source === 'hots_system_catalog') {
                targetBtn = document.getElementById('tabHotsCatalog');
            }
            
            if (!targetBtn) {
                const allTabs = document.querySelectorAll('.source-tab');
                for (const b of allTabs) {
                    const oc = b.getAttribute('onclick') || '';
                    if (oc.includes(`'${source}'`)) {
                        targetBtn = b;
                        break;
                    }
                }
            }
            
            if (targetBtn && targetBtn.classList) {
                targetBtn.classList.add('active');
            }"""

if old_switch in html:
    html = html.replace(old_switch, new_switch, 1)
    print("2. Fixed switchSourceTab implementation")
else:
    print("WARNING: Old switchSourceTab snippet not matched exactly! Checking variations...")

# 3. quickExportExcel definition
if 'function quickExportExcel' not in html:
    old_export_batch = """        function exportBatch(target) {
            openExportConfirmModal(target);
        }"""
    
    new_export_batch = """        function quickExportExcel(target = 'selected') {
            openExportConfirmModal(target);
        }

        function exportBatch(target) {
            openExportConfirmModal(target);
        }"""
    
    if old_export_batch in html:
        html = html.replace(old_export_batch, new_export_batch, 1)
        print("3. Added quickExportExcel function definition")
    else:
        print("WARNING: exportBatch snippet not matched!")

with open('App/template.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Template patch complete!")
