# -*- coding: utf-8 -*-
"""
Patch App/template.html with:
1. Shopee Selection Control Bar (Pilih Semua, Terpilih Counter, Buat Image Gen).
2. Card selection checkbox and [⚡ Buat Image Gen] action button.
3. JavaScript functions for selection and custom Photobank generation without MCP.
"""
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    with open('App/template.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Insert Shopee Selection Bar right after Filter Toolbar in renderShopeeStudio
    old_toolbar_end = '''                    <!-- Filter Toolbar -->
                    <div style="display: flex; gap: 12px; align-items: center; flex-wrap: wrap; background: #ffffff; padding: 10px 14px; border-radius: 10px; border: 1px solid #fed7aa;">
                        <div style="flex: 1; min-width: 260px; position: relative;">
                            <input type="text" id="shopeeSearchInput" value="${shopeeSearchFilter}" placeholder="Cari nama produk, SKU, atau folder..." oninput="onShopeeSearch(this.value)" style="width: 100%; padding: 8px 12px; border: 1px solid var(--border); border-radius: 6px; font-size: 0.88rem;">
                        </div>
                        <div style="display: flex; gap: 10px; align-items: center;">
                            <select id="shopeeBrandSelect" onchange="onShopeeBrandFilter(this.value)" style="padding: 8px 12px; border: 1px solid var(--border); border-radius: 6px; font-size: 0.85rem; font-weight: 700; color: #334155;">
                                <option value="all" ${shopeeBrandFilter === 'all' ? 'selected' : ''}>Semua Brand (${totalCount})</option>
                                <option value="AP Boots" ${shopeeBrandFilter === 'AP Boots' ? 'selected' : ''}>AP Boots Official (${apCount})</option>
                                <option value="Petrova" ${shopeeBrandFilter === 'Petrova' ? 'selected' : ''}>Petrova Official (${petrovaCount})</option>
                            </select>
                            <span style="font-size: 0.82rem; font-weight: 700; color: #64748b;">Menampilkan: ${filtered.length} produk</span>
                        </div>
                    </div>
                </div>

                <!-- Products Grid -->'''

    new_toolbar_end = '''                    <!-- Filter Toolbar -->
                    <div style="display: flex; gap: 12px; align-items: center; flex-wrap: wrap; background: #ffffff; padding: 10px 14px; border-radius: 10px; border: 1px solid #fed7aa;">
                        <div style="flex: 1; min-width: 260px; position: relative;">
                            <input type="text" id="shopeeSearchInput" value="${shopeeSearchFilter}" placeholder="Cari nama produk, SKU, atau folder..." oninput="onShopeeSearch(this.value)" style="width: 100%; padding: 8px 12px; border: 1px solid var(--border); border-radius: 6px; font-size: 0.88rem;">
                        </div>
                        <div style="display: flex; gap: 10px; align-items: center;">
                            <select id="shopeeBrandSelect" onchange="onShopeeBrandFilter(this.value)" style="padding: 8px 12px; border: 1px solid var(--border); border-radius: 6px; font-size: 0.85rem; font-weight: 700; color: #334155;">
                                <option value="all" ${shopeeBrandFilter === 'all' ? 'selected' : ''}>Semua Brand (${totalCount})</option>
                                <option value="AP Boots" ${shopeeBrandFilter === 'AP Boots' ? 'selected' : ''}>AP Boots Official (${apCount})</option>
                                <option value="Petrova" ${shopeeBrandFilter === 'Petrova' ? 'selected' : ''}>Petrova Official (${petrovaCount})</option>
                            </select>
                            <span style="font-size: 0.82rem; font-weight: 700; color: #64748b;">Menampilkan: ${filtered.length} produk</span>
                        </div>
                    </div>

                    <!-- Shopee Studio Selection & Bulk Image Gen Bar -->
                    <div style="background: #ffffff; border: 1px solid #fed7aa; border-radius: 10px; padding: 10px 16px; margin-top: 12px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; box-shadow: 0 1px 3px rgba(234, 88, 12, 0.08);">
                        <div style="display: flex; align-items: center; gap: 14px; flex-wrap: wrap;">
                            <label style="display: flex; align-items: center; gap: 8px; font-size: 0.85rem; font-weight: 700; color: #9a3412; cursor: pointer; user-select: none;">
                                <input type="checkbox" id="selectAllShopeeCheckbox" onchange="toggleSelectAllShopee(this.checked)" style="width: 18px; height: 18px; accent-color: #ea580c; cursor: pointer;">
                                <span>Pilih Semua yang Tampil</span>
                            </label>
                            <span style="color: #fed7aa;">|</span>
                            <span style="font-size: 0.85rem; color: #64748b;">
                                Terpilih: <strong id="shopeeSelCount" style="color: #ea580c; font-size: 1.05rem; font-weight: 800;">${selectedShopeeFolders.size}</strong> produk
                            </span>
                            <button type="button" class="btn btn-sm" onclick="selectAllShopeeProducts()" style="background: #fff7ed; border: 1px solid #fdba74; color: #c2410c; font-size: 0.75rem; padding: 5px 12px; border-radius: 6px; font-weight: 700;">
                                Pilih Semua (${totalCount})
                            </button>
                            <button type="button" class="btn btn-sm" onclick="clearShopeeSelection()" id="btnClearShopeeSel" style="${selectedShopeeFolders.size > 0 ? '' : 'display: none;'} background: #f1f5f9; border: 1px solid #cbd5e1; color: #475569; font-size: 0.75rem; padding: 5px 12px; border-radius: 6px; font-weight: 700;">
                                Batalkan Pilihan
                            </button>
                        </div>
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <button type="button" class="btn btn-sm" onclick="openPhotobankGenModalForSelected()" id="btnGenShopeeSelected" style="background: linear-gradient(135deg, #059669, #047857); color: #fff; font-weight: 800; font-size: 0.84rem; border-radius: 8px; padding: 8px 18px; box-shadow: 0 3px 8px rgba(5, 150, 105, 0.35); cursor: pointer;">
                                ⚡ Buat Image Generation (${selectedShopeeFolders.size > 0 ? selectedShopeeFolders.size + ' Terpilih' : 'Pilih Produk'})
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Products Grid -->'''

    if old_toolbar_end in html:
        html = html.replace(old_toolbar_end, new_toolbar_end, 1)
        print("1. Inserted Shopee Selection Control Bar successfully!")
    else:
        print("WARNING: old_toolbar_end not matched!")

    # 2. Update Card Header with Checkbox & Selection highlight
    old_card_header = '''                        <!-- Card Header -->
                        <div class="shopee-card-header">
                            <div style="display: flex; align-items: center; gap: 8px;">
                                <span class="shopee-badge-sku">${p.sku}</span>
                                <span class="shopee-badge-brand ${brandClass}">${p.brand}</span>
                            </div>
                            <div style="font-size: 0.92rem; font-weight: 800; color: #0f172a;">
                                Rp ${p.price_idr || '-'}
                            </div>
                        </div>'''

    new_card_header = '''                        <!-- Card Header -->
                        <div class="shopee-card-header">
                            <div style="display: flex; align-items: center; gap: 8px;">
                                <input type="checkbox" class="shopee-card-checkbox" value="${p.folder_name}" ${selectedShopeeFolders.has(p.folder_name) ? 'checked' : ''} onchange="toggleShopeeCardSelection('${p.folder_name}', '${p.sku}', this.checked)" style="width: 17px; height: 17px; accent-color: #059669; cursor: pointer;">
                                <span class="shopee-badge-sku">${p.sku}</span>
                                <span class="shopee-badge-brand ${brandClass}">${p.brand}</span>
                            </div>
                            <div style="font-size: 0.92rem; font-weight: 800; color: #0f172a;">
                                Rp ${p.price_idr || '-'}
                            </div>
                        </div>'''

    if old_card_header in html:
        html = html.replace(old_card_header, new_card_header, 1)
        print("2. Updated Card Header with Selection Checkbox successfully!")
    else:
        print("WARNING: old_card_header not matched!")

    # 3. Add [⚡ Buat Image Gen] button in card actions row
    old_card_actions = '''                        <!-- Action Buttons -->
                        <div class="shopee-actions-row">
                            <button type="button" class="btn btn-sm" onclick="openFlowModal('${p.sku}', '${p.folder_name}', '${p.product_name.replace(/'/g, "\\\\'")}')" style="background: linear-gradient(135deg, #059669, #047857); color: #fff; font-weight: 700; font-size: 0.76rem; border-radius: 6px; padding: 7px 10px;" title="Google Flow 4-Slot Studio & Photobank Upload">
                                ⚡ Flow & Photobank
                            </button>
                            <button type="button" class="btn btn-sm" onclick="openShopeeJsonModal('${p.folder_name}', '${p.product_name.replace(/'/g, "\\\\'")}')" style="flex: 1; background: #f8fafc; border: 1px solid var(--border); color: #0f172a; font-weight: 700; font-size: 0.76rem; border-radius: 6px; padding: 7px 10px;">
                                📄 View Alibaba JSON
                            </button>'''

    new_card_actions = '''                        <!-- Action Buttons -->
                        <div class="shopee-actions-row">
                            <button type="button" class="btn btn-sm" onclick="openPhotobankGenModalForSingle('${p.sku}', '${p.folder_name}', '${p.product_name.replace(/'/g, "\\\\'")}')" style="background: linear-gradient(135deg, #059669, #047857); color: #fff; font-weight: 700; font-size: 0.76rem; border-radius: 6px; padding: 7px 10px;" title="Buat Image Generation Kustom (Tanpa MCP)">
                                ⚡ Buat Image Gen
                            </button>
                            <button type="button" class="btn btn-sm" onclick="openFlowModal('${p.sku}', '${p.folder_name}', '${p.product_name.replace(/'/g, "\\\\'")}')" style="background: #f0fdf4; border: 1px solid #bbf7d0; color: #166534; font-weight: 700; font-size: 0.76rem; border-radius: 6px; padding: 7px 10px;" title="Google Flow 4-Slot Studio & Photobank Upload">
                                🌐 Flow Studio
                            </button>
                            <button type="button" class="btn btn-sm" onclick="openShopeeJsonModal('${p.folder_name}', '${p.product_name.replace(/'/g, "\\\\'")}')" style="flex: 1; background: #f8fafc; border: 1px solid var(--border); color: #0f172a; font-weight: 700; font-size: 0.76rem; border-radius: 6px; padding: 7px 10px;">
                                📄 JSON
                            </button>'''

    if old_card_actions in html:
        html = html.replace(old_card_actions, new_card_actions, 1)
        print("3. Updated Card Action Row with [⚡ Buat Image Gen] successfully!")
    else:
        print("WARNING: old_card_actions not matched!")

    # 4. Insert Selection & Modal JavaScript logic before </script>
    js_target = '''        // Google Flow & Photobank Admin Studio Logic'''
    
    new_js_logic = '''        // Shopee Studio Selection & Standalone Photobank Image Gen Logic (Tanpa MCP)
        const selectedShopeeFolders = new Set();
        let currentModalTargetItems = [];

        function toggleShopeeCardSelection(folder, sku, isChecked) {
            if (isChecked) {
                selectedShopeeFolders.add(folder);
            } else {
                selectedShopeeFolders.delete(folder);
            }
            updateShopeeSelectionDisplay();
        }

        function toggleSelectAllShopee(isChecked) {
            const filtered = shopeeProductsData.filter(p => {
                if (shopeeBrandFilter !== 'all' && p.brand !== shopeeBrandFilter) return false;
                if (shopeeSearchFilter) {
                    const q = shopeeSearchFilter.toLowerCase();
                    const matchName = (p.product_name || '').toLowerCase().includes(q);
                    const matchSku = (p.sku || '').toLowerCase().includes(q);
                    const matchFolder = (p.folder_name || '').toLowerCase().includes(q);
                    if (!matchName && !matchSku && !matchFolder) return false;
                }
                return true;
            });

            if (isChecked) {
                filtered.forEach(p => selectedShopeeFolders.add(p.folder_name));
            } else {
                filtered.forEach(p => selectedShopeeFolders.delete(p.folder_name));
            }
            renderShopeeStudio();
        }

        function selectAllShopeeProducts() {
            shopeeProductsData.forEach(p => selectedShopeeFolders.add(p.folder_name));
            renderShopeeStudio();
            showToast(`✓ Memilih seluruh ${shopeeProductsData.length} produk Shopee!`);
        }

        function clearShopeeSelection() {
            selectedShopeeFolders.clear();
            renderShopeeStudio();
            showToast('Pilihan produk dibatalkan.');
        }

        function updateShopeeSelectionDisplay() {
            const count = selectedShopeeFolders.size;
            const counter = document.getElementById('shopeeSelCount');
            if (counter) counter.innerText = count;
            
            const btnClear = document.getElementById('btnClearShopeeSel');
            if (btnClear) btnClear.style.display = count > 0 ? 'inline-block' : 'none';
            
            const btnGen = document.getElementById('btnGenShopeeSelected');
            if (btnGen) {
                btnGen.innerHTML = `⚡ Buat Image Generation (${count > 0 ? count + ' Terpilih' : 'Pilih Produk'})`;
            }
        }

        function openPhotobankGenModalForSelected() {
            if (selectedShopeeFolders.size === 0) {
                alert('Silakan pilih minimal 1 produk terlebih dahulu menggunakan centang kotak pada kartu produk.');
                return;
            }
            
            currentModalTargetItems = [];
            selectedShopeeFolders.forEach(folder => {
                const prod = shopeeProductsData.find(p => p.folder_name === folder);
                if (prod) {
                    currentModalTargetItems.push({
                        sku: prod.sku,
                        folder: prod.folder_name,
                        product_name: prod.product_name
                    });
                }
            });

            populatePhotobankGenModal();
            document.getElementById('photobankGenModal').classList.add('active');
        }

        function openPhotobankGenModalForSingle(sku, folder, productName) {
            currentModalTargetItems = [{
                sku: sku,
                folder: folder,
                product_name: productName
            }];

            populatePhotobankGenModal();
            document.getElementById('photobankGenModal').classList.add('active');
        }

        function populatePhotobankGenModal() {
            const count = currentModalTargetItems.length;
            document.getElementById('genModalTargetCount').innerText = `${count} Produk Terpilih`;
            
            let listHtml = '';
            currentModalTargetItems.forEach((it, idx) => {
                listHtml += `${idx + 1}. [${it.sku}] ${it.product_name} (${it.folder})\\n`;
            });
            document.getElementById('genModalSelectedList').innerText = listHtml || 'Tidak ada produk terpilih';
            
            document.getElementById('genModalProgressBar').style.width = '0%';
            document.getElementById('genModalLogStatus').innerText = 'Siap Eksekusi';
            document.getElementById('genModalLogBox').innerText = `Siap memproses ${count} produk dengan mesin native (tanpa MCP).\\nPilih slot gambar di atas lalu klik 'Mulai Generate'.`;
            
            const btn = document.getElementById('btnExecuteGenModal');
            if (btn) {
                btn.disabled = false;
                btn.innerHTML = `⚡ Mulai Generate Foto (${count} Produk - Native Engine)`;
            }
        }

        function applySlotPreset(preset) {
            const chk1 = document.getElementById('chkSlot1');
            const chk2 = document.getElementById('chkSlot2');
            const chk3 = document.getElementById('chkSlot3');
            const chk4 = document.getElementById('chkSlot4');

            if (preset === 'all') {
                chk1.checked = true; chk2.checked = true; chk3.checked = true; chk4.checked = true;
                showToast('Preset: Semua 4 Slot Aktif');
            } else if (preset === 'hero_side') {
                chk1.checked = true; chk2.checked = true; chk3.checked = false; chk4.checked = false;
                showToast('Preset: Hanya Hero & Side Aktif');
            } else if (preset === 'tread_usage') {
                chk1.checked = false; chk2.checked = false; chk3.checked = true; chk4.checked = true;
                showToast('Preset: Hanya Tapak & Contextual Aktif');
            }
        }

        async function executeCustomPhotobankGeneration() {
            if (currentModalTargetItems.length === 0) {
                alert('Tidak ada produk yang dipilih.');
                return;
            }

            // Gather options
            const slots = [];
            if (document.getElementById('chkSlot1').checked) slots.push(1);
            if (document.getElementById('chkSlot2').checked) slots.push(2);
            if (document.getElementById('chkSlot3').checked) slots.push(3);
            if (document.getElementById('chkSlot4').checked) slots.push(4);

            if (slots.length === 0) {
                alert('Silakan pilih minimal 1 opsi variasi slot gambar yang ingin dibuat!');
                return;
            }

            const targetSize = parseInt(document.getElementById('genOptSize').value) || 1000;
            const fillRatio = parseFloat(document.getElementById('genOptFill').value) || 0.85;
            const saveShopee = document.getElementById('chkSaveShopee').checked;
            const saveFlow = document.getElementById('chkSaveFlow').checked;
            const savePhotobank = document.getElementById('chkSavePhotobank').checked;

            const btn = document.getElementById('btnExecuteGenModal');
            btn.disabled = true;
            btn.innerHTML = '⏳ Sedang Memproses Generator...';

            const logBox = document.getElementById('genModalLogBox');
            const pBar = document.getElementById('genModalProgressBar');
            const statusLbl = document.getElementById('genModalLogStatus');

            logBox.innerText = `Memulai Image Generation untuk ${currentModalTargetItems.length} produk...\\nSlots dipilih: [${slots.join(', ')}] | Resolusi: ${targetSize}x${targetSize} | Fill: ${fillRatio*100}%\\n`;
            statusLbl.innerText = 'Memproses...';

            const total = currentModalTargetItems.length;
            let successCount = 0;

            for (let i = 0; i < total; i++) {
                const item = currentModalTargetItems[i];
                const pct = Math.round(((i + 1) / total) * 100);
                pBar.style.width = `${pct}%`;
                statusLbl.innerText = `Memproses ${i + 1}/${total} (${pct}%)...`;

                logBox.innerText += `\\n[${i + 1}/${total}] Memproses ${item.sku} (${item.folder})...\\n`;
                logBox.scrollTop = logBox.scrollHeight;

                try {
                    const res = await fetch('/api/photobank/custom-generate', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            sku: item.sku,
                            folder: item.folder,
                            slots: slots,
                            target_size: targetSize,
                            fill_ratio: fillRatio,
                            save_to_shopee: saveShopee,
                            save_to_flow: saveFlow,
                            save_to_photobank: savePhotobank
                        })
                    });
                    const data = await res.json();
                    if (data.success) {
                        successCount++;
                        logBox.innerText += `  ✓ Berhasil! Dibuat ${data.variations_generated.length} slot variasi (Kategori: ${data.category_folder})\\n`;
                        for (const v of data.variations_generated) {
                            logBox.innerText += `    - Slot ${v.slot} (${v.type}): ${v.filename}\\n`;
                        }
                    } else {
                        logBox.innerText += `  ❌ Gagal: ${data.error}\\n`;
                    }
                } catch (err) {
                    logBox.innerText += `  ❌ Network Error: ${err}\\n`;
                }
                logBox.scrollTop = logBox.scrollHeight;
            }

            pBar.style.width = '100%';
            statusLbl.innerText = `Selesai! (${successCount}/${total} Berhasil)`;
            logBox.innerText += `\\n=======================================================\\n🎉 SELESAI! ${successCount} dari ${total} produk berhasil digenerate sempurna!\\n`;
            logBox.scrollTop = logBox.scrollHeight;

            btn.disabled = false;
            btn.innerHTML = '⚡ Mulai Generate Foto Baru';

            showToast(`✓ Sukses membuat variasi foto untuk ${successCount} produk!`);
            
            // Refresh shopee studio view so new images reflect
            setTimeout(() => {
                loadShopeeStudioView();
            }, 800);
        }\n\n'''

    if js_target in html and 'const selectedShopeeFolders = new Set();' not in html:
        html = html.replace(js_target, new_js_logic + js_target, 1)
        print("4. Inserted Selection & Generator JavaScript logic successfully!")
    else:
        print("Notice: JavaScript logic already present or js_target not found.")

    with open('App/template.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    main()
