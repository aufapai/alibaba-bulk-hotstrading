# -*- coding: utf-8 -*-
"""
Patch App/template.html:
1. Add .modal-overlay.active { display: flex !important; } to CSS.
2. In Shopee Studio, remove the fake side image and display single prominent Hero image.
3. Update metrics to remove fake side view metric.
4. Enhance selection with prominent green border, checkbox, and 'TERPILIH' badge.
5. Fix openPhotobankGenModalForSelected and openPhotobankGenModalForSingle to open with style.display='flex' & classList.add('active').
"""
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    with open('App/template.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Add .modal-overlay.active CSS
    if '.modal-overlay.active' not in html:
        css_target = '.modal-overlay {'
        css_replacement = '.modal-overlay.active {\n            display: flex !important;\n        }\n        .modal-overlay {'
        html = html.replace(css_target, css_replacement, 1)
        print("1. Added .modal-overlay.active CSS successfully!")

    # 2. Update Shopee Metrics Grid (remove fake side view count)
    old_metrics = '''                    <!-- Metrics Grid -->
                    <div class="shopee-studio-metrics">
                        <div class="shopee-metric-card">
                            <div class="shopee-metric-num">${totalCount}</div>
                            <div class="shopee-metric-lbl">Total Produk Resmi (${apCount} AP Boots + ${petrovaCount} Petrova)</div>
                        </div>
                        <div class="shopee-metric-card">
                            <div class="shopee-metric-num" style="color: #059669;">${heroReadyCount} / ${totalCount}</div>
                            <div class="shopee-metric-lbl">Hero WEBP Ready (hero_*.webp)</div>
                        </div>
                        <div class="shopee-metric-card">
                            <div class="shopee-metric-num" style="color: #0284c7;">${sideReadyCount} / ${totalCount}</div>
                            <div class="shopee-metric-lbl">Side View White BG Ready (side_*.webp)</div>
                        </div>
                        <div class="shopee-metric-card">
                            <div class="shopee-metric-num" style="color: #7c3aed;">${jsonReadyCount} / ${totalCount}</div>
                            <div class="shopee-metric-lbl">Alibaba B2B JSON Specs Ready</div>
                        </div>
                    </div>'''

    new_metrics = '''                    <!-- Metrics Grid (Hero-First Official Reference) -->
                    <div class="shopee-studio-metrics">
                        <div class="shopee-metric-card">
                            <div class="shopee-metric-num">${totalCount}</div>
                            <div class="shopee-metric-lbl">Total Produk Resmi (${apCount} AP Boots + ${petrovaCount} Petrova)</div>
                        </div>
                        <div class="shopee-metric-card">
                            <div class="shopee-metric-num" style="color: #059669;">${heroReadyCount} / ${totalCount}</div>
                            <div class="shopee-metric-lbl">Hero WEBP Ready (hero_*.webp)</div>
                        </div>
                        <div class="shopee-metric-card">
                            <div class="shopee-metric-num" style="color: #0284c7;">4 Variasi Slot</div>
                            <div class="shopee-metric-lbl">Photobank Generator (Hero, Side, Tread, Usage)</div>
                        </div>
                        <div class="shopee-metric-card">
                            <div class="shopee-metric-num" style="color: #7c3aed;">${jsonReadyCount} / ${totalCount}</div>
                            <div class="shopee-metric-lbl">Alibaba B2B JSON Specs Ready</div>
                        </div>
                    </div>'''

    if old_metrics in html:
        html = html.replace(old_metrics, new_metrics, 1)
        print("2. Updated Metrics Grid (removed fake side view metric)!")
    else:
        print("Notice: old_metrics not matched, checking...")

    # 3. Replace card rendering to remove dual-image (only hero) and add selected styling
    old_card_loop = '''                    html += `
                    <div class="shopee-card" id="card-${p.folder_name}">
                        <!-- Card Header -->
                        <div class="shopee-card-header">
                            <div style="display: flex; align-items: center; gap: 8px;">
                                <input type="checkbox" class="shopee-card-checkbox" value="${p.folder_name}" ${selectedShopeeFolders.has(p.folder_name) ? 'checked' : ''} onchange="toggleShopeeCardSelection('${p.folder_name}', '${p.sku}', this.checked)" style="width: 17px; height: 17px; accent-color: #059669; cursor: pointer;">
                                <span class="shopee-badge-sku">${p.sku}</span>
                                <span class="shopee-badge-brand ${brandClass}">${p.brand}</span>
                            </div>
                            <div style="font-size: 0.92rem; font-weight: 800; color: #0f172a;">
                                Rp ${p.price_idr || '-'}
                            </div>
                        </div>

                        <!-- Product Title -->
                        <div>
                            <div style="font-size: 0.92rem; font-weight: 700; color: #0f172a; line-height: 1.35; margin-bottom: 5px;">
                                ${p.product_name}
                            </div>
                            <div style="display: flex; gap: 10px; font-size: 0.72rem; color: #64748b;">
                                <span>🛒 ${p.sold_count || 'Official Store'}</span>
                                <span>⭐ ${p.rating || '4.9'}</span>
                                <span style="font-family: monospace; color: #94a3b8;">📁 ${p.folder_name.substring(0, 30)}...</span>
                            </div>
                        </div>

                        <!-- Dual Image View (Hero + Side View on White BG) -->
                        <div class="shopee-dual-image-row">
                            <!-- Hero Image -->
                            <div class="shopee-img-box">
                                <img src="${heroSrc}" alt="Hero Image" id="img-hero-${p.folder_name}" loading="lazy" onclick="window.open(this.src)">
                                <div class="shopee-img-label">
                                    <span>🌟</span>
                                    <span>Hero: <code>${p.hero_filename.substring(0, 16)}...</code></span>
                                </div>
                                <span style="font-size: 0.68rem; color: ${p.hero_exists ? '#059669' : '#d97706'}; font-weight: 700;">
                                    ${p.hero_exists ? '✅ Local WEBP' : '⚠️ Online CDN'}
                                </span>
                            </div>

                            <!-- Side View Image (White BG) -->
                            <div class="shopee-img-box">
                                <img src="${sideSrc}" alt="Side View Image" id="img-side-${p.folder_name}" loading="lazy" onclick="window.open(this.src)">
                                <div class="shopee-img-label">
                                    <span>📐</span>
                                    <span>Side: <code>${p.side_filename.substring(0, 16)}...</code></span>
                                </div>
                                <span style="font-size: 0.68rem; color: ${p.side_exists ? '#0284c7' : '#94a3b8'}; font-weight: 700;">
                                    ${p.side_exists ? '✅ White BG Studio' : '⚠️ Belum Ada'}
                                </span>
                            </div>
                        </div>

                        <!-- Automated Image Inserter Dropzone -->
                        <div class="shopee-dropzone-box" 
                             ondragover="handleShopeeDragOver(event)" 
                             ondragleave="handleShopeeDragLeave(event)" 
                             ondrop="handleShopeeDrop(event, '${p.folder_name}')"
                             onclick="triggerShopeeFileInput('${p.folder_name}')">
                            <div class="shopee-dropzone-title">
                                <span>📤</span> Drag & Drop Foto Baru atau Klik untuk Input Foto
                            </div>
                            <div class="shopee-upload-options" onclick="event.stopPropagation()">
                                <label style="display: flex; align-items: center; gap: 4px; cursor: pointer;">
                                    <input type="radio" name="upload_target_${p.folder_name}" value="hero" checked>
                                    <span>Jadikan Hero (hero_*.webp)</span>
                                </label>
                                <label style="display: flex; align-items: center; gap: 4px; cursor: pointer;">
                                    <input type="radio" name="upload_target_${p.folder_name}" value="side">
                                    <span>Jadikan Side (side_*.webp)</span>
                                </label>
                            </div>
                            <input type="file" id="file-${p.folder_name}" accept="image/*" style="display: none;" onchange="handleShopeeFileSelect(event, '${p.folder_name}')">
                        </div>'''

    new_card_loop = '''                    const isSelected = selectedShopeeFolders.has(p.folder_name);
                    html += `
                    <div class="shopee-card ${isSelected ? 'selected' : ''}" id="card-${p.folder_name}" style="${isSelected ? 'border: 2px solid #059669; background: #f0fdf4; box-shadow: 0 4px 16px rgba(5, 150, 105, 0.18);' : ''}">
                        <!-- Card Header with Clear Selection Checkbox & Toggle -->
                        <div class="shopee-card-header" style="cursor: pointer;" onclick="toggleShopeeCardSelection('${p.folder_name}', '${p.sku}', ${!isSelected})">
                            <div style="display: flex; align-items: center; gap: 8px;">
                                <input type="checkbox" class="shopee-card-checkbox" value="${p.folder_name}" ${isSelected ? 'checked' : ''} onclick="event.stopPropagation()" onchange="toggleShopeeCardSelection('${p.folder_name}', '${p.sku}', this.checked)" style="width: 18px; height: 18px; accent-color: #059669; cursor: pointer;">
                                <span class="shopee-badge-sku">${p.sku}</span>
                                <span class="shopee-badge-brand ${brandClass}">${p.brand}</span>
                                ${isSelected ? '<span style="background: #059669; color: #fff; font-size: 0.68rem; font-weight: 800; padding: 2px 7px; border-radius: 4px;">✓ TERPILIH</span>' : ''}
                            </div>
                            <div style="font-size: 0.92rem; font-weight: 800; color: #0f172a;">
                                Rp ${p.price_idr || '-'}
                            </div>
                        </div>

                        <!-- Product Title -->
                        <div>
                            <div style="font-size: 0.92rem; font-weight: 700; color: #0f172a; line-height: 1.35; margin-bottom: 5px;">
                                ${p.product_name}
                            </div>
                            <div style="display: flex; gap: 10px; font-size: 0.72rem; color: #64748b;">
                                <span>🛒 ${p.sold_count || 'Official Store'}</span>
                                <span>⭐ ${p.rating || '4.9'}</span>
                                <span style="font-family: monospace; color: #94a3b8;">📁 ${p.folder_name.substring(0, 30)}...</span>
                            </div>
                        </div>

                        <!-- Single Prominent Hero Image (Official Shopee Reference Only - No Fake Side) -->
                        <div class="shopee-single-image-wrap" style="width: 100%; aspect-ratio: 1/1; background: #f8fafc; border: 1px solid var(--border); border-radius: 8px; overflow: hidden; display: flex; flex-direction: column; position: relative;">
                            <div style="flex: 1; display: flex; align-items: center; justify-content: center; overflow: hidden; padding: 8px;">
                                <img src="${heroSrc}" alt="Hero Image" id="img-hero-${p.folder_name}" loading="lazy" onclick="window.open(this.src)" style="width: 100%; height: 100%; object-fit: contain; cursor: pointer; transition: transform 0.2s ease;">
                            </div>
                            <div class="shopee-img-label" style="background: rgba(15, 23, 42, 0.88); color: #fff; padding: 6px 10px; font-size: 0.72rem; display: flex; justify-content: space-between; align-items: center;">
                                <span style="display: flex; align-items: center; gap: 4px;">
                                    <span>🌟</span>
                                    <span>Hero: <code>${p.hero_filename.substring(0, 22)}...</code></span>
                                </span>
                                <span style="color: ${p.hero_exists ? '#34d399' : '#fbbf24'}; font-weight: 700;">
                                    ${p.hero_exists ? '✅ Local WEBP' : '⚠️ Online CDN'}
                                </span>
                            </div>
                        </div>

                        <!-- Automated Hero Image Inserter Dropzone -->
                        <div class="shopee-dropzone-box" 
                             ondragover="handleShopeeDragOver(event)" 
                             ondragleave="handleShopeeDragLeave(event)" 
                             ondrop="handleShopeeDrop(event, '${p.folder_name}')"
                             onclick="triggerShopeeFileInput('${p.folder_name}')">
                            <div class="shopee-dropzone-title">
                                <span>📤</span> Drag & Drop Foto Hero Baru atau Klik untuk Ganti
                            </div>
                            <div style="font-size: 0.7rem; color: #9a3412; margin-top: 3px;">
                                Otomatis disimpan sebagai <code>hero_${p.folder_name}.webp</code>
                            </div>
                            <input type="file" id="file-${p.folder_name}" accept="image/*" style="display: none;" onchange="handleShopeeFileSelect(event, '${p.folder_name}')">
                        </div>'''

    if old_card_loop in html:
        html = html.replace(old_card_loop, new_card_loop, 1)
        print("3. Replaced dual-image row with Single Hero Image & updated selection visual!")
    else:
        print("WARNING: old_card_loop not matched!")

    # 4. Fix openPhotobankGenModalForSelected, openPhotobankGenModalForSingle, and toggleShopeeCardSelection in JS
    old_gen_js = '''        function toggleShopeeCardSelection(folder, sku, isChecked) {
            if (isChecked) {
                selectedShopeeFolders.add(folder);
            } else {
                selectedShopeeFolders.delete(folder);
            }
            updateShopeeSelectionDisplay();
        }'''

    new_gen_js = '''        function toggleShopeeCardSelection(folder, sku, isChecked) {
            if (isChecked) {
                selectedShopeeFolders.add(folder);
            } else {
                selectedShopeeFolders.delete(folder);
            }
            // Dynamically update card styling without re-rendering entire grid
            const card = document.getElementById(`card-${folder}`);
            if (card) {
                if (isChecked) {
                    card.classList.add('selected');
                    card.style.border = '2px solid #059669';
                    card.style.background = '#f0fdf4';
                    card.style.boxShadow = '0 4px 16px rgba(5, 150, 105, 0.18)';
                } else {
                    card.classList.remove('selected');
                    card.style.border = '';
                    card.style.background = '';
                    card.style.boxShadow = '';
                }
                const chk = card.querySelector('.shopee-card-checkbox');
                if (chk) chk.checked = isChecked;
            }
            updateShopeeSelectionDisplay();
        }'''

    if old_gen_js in html:
        html = html.replace(old_gen_js, new_gen_js, 1)
        print("4. Updated toggleShopeeCardSelection with live dynamic card highlighting!")

    # 5. Fix openPhotobankGenModalForSelected to guarantee modal visibility
    old_open_modal = '''            populatePhotobankGenModal();
            document.getElementById('photobankGenModal').classList.add('active');
        }'''

    new_open_modal = '''            populatePhotobankGenModal();
            const modal = document.getElementById('photobankGenModal');
            if (modal) {
                modal.style.display = 'flex';
                modal.classList.add('active');
            }
        }'''

    if old_open_modal in html:
        html = html.replace(old_open_modal, new_open_modal)
        print("5. Fixed openPhotobankGenModal to display='flex' & classList.add('active')!")

    # 6. Fix closeModal to ensure style.display='none' & classList.remove('active')
    old_close_modal = '''        function closeModal(modalId) {
            document.getElementById(modalId).style.display = 'none';
        }'''

    new_close_modal = '''        function closeModal(modalId) {
        const el = document.getElementById(modalId);
        if (el) {
            el.style.display = 'none';
            el.classList.remove('active');
        }
    }'''

    if old_close_modal in html:
        html = html.replace(old_close_modal, new_close_modal, 1)
        print("6. Updated closeModal to remove active class and set display none!")

    # 7. In processShopeeUpload, force upload target to hero
    old_upload_target = "const target = card.querySelector(`input[name=\"upload_target_${folder}\"]:checked`).value || 'hero';"
    new_upload_target = "const target = 'hero';"
    if old_upload_target in html:
        html = html.replace(old_upload_target, new_upload_target, 1)
        print("7. Updated upload target to strictly 'hero'!")

    with open('App/template.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("ALL FIXES APPLIED SUCCESSFULLY TO App/template.html!")

if __name__ == '__main__':
    main()
