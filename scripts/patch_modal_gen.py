# -*- coding: utf-8 -*-
"""
Patch App/template.html with:
1. Modal #photobankGenModal (Standalone Image Generation Studio - Tanpa MCP)
2. Selection Bar & Card Checkboxes in Shopee Studio
3. JavaScript functions for selecting products and executing custom image gen.
"""
import sys

def main():
    with open('App/template.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Insert #photobankGenModal after #flowPhotobankModal
    target_modal_end = '''    <!-- MODAL 9: GOOGLE FLOW & PHOTOBANK ADMIN STUDIO -->'''
    
    new_gen_modal = '''    <!-- MODAL 10: PHOTOBANK IMAGE GENERATION STUDIO (STANDALONE - TANPA MCP) -->
    <div class="modal-overlay" id="photobankGenModal">
        <div class="modal-content" style="max-width: 950px; max-height: 92vh; display: flex; flex-direction: column;">
            <div class="modal-header" style="background: linear-gradient(135deg, #065f46, #047857); color: #ffffff; padding: 1.1rem 1.5rem; border-top-left-radius: 12px; border-top-right-radius: 12px;">
                <div style="flex: 1;">
                    <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
                        <span style="font-size: 1.6rem;">⚡</span>
                        <h3 style="font-size: 1.25rem; font-weight: 800; color: #ffffff; margin: 0;">
                            Studio Image Generation Photobank (Standalone Engine — Tanpa MCP)
                        </h3>
                        <span class="badge" style="background: #10b981; color: #ffffff; font-size: 0.75rem; padding: 3px 8px; border-radius: 6px;">
                            Native Python / PIL
                        </span>
                    </div>
                    <div style="font-size: 0.8rem; color: #a7f3d0; margin-top: 6px;">
                        Pilih opsi variasi gambar produk yang ingin dibuat, resolusi kanvas, dan rasio bingkai tanpa dependensi eksternal.
                    </div>
                </div>
                <button class="btn-close" style="color: #fff; opacity: 0.85;" onclick="closeModal('photobankGenModal')">&times;</button>
            </div>
            
            <div class="modal-body" style="padding: 1.25rem; overflow-y: auto; background: #f8fafc; flex: 1;">
                <!-- Selected Products Summary Banner -->
                <div style="background: #ffffff; border: 1px solid #fed7aa; border-radius: 10px; padding: 12px 16px; margin-bottom: 16px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <span style="font-size: 0.85rem; font-weight: 800; color: #9a3412;">
                            📦 Target Produk yang Diproses: <strong id="genModalTargetCount" style="color: #ea580c;">0 Produk</strong>
                        </span>
                        <span style="font-size: 0.75rem; color: #64748b;" id="genModalTargetBadge">Siap Dibuat</span>
                    </div>
                    <div id="genModalSelectedList" style="max-height: 80px; overflow-y: auto; font-size: 0.75rem; color: #475569; background: #fff7ed; padding: 8px 12px; border-radius: 6px; border: 1px solid #fed7aa; font-family: monospace;">
                        -
                    </div>
                </div>

                <!-- Section: Pilihan Slot / Variasi Gambar -->
                <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px 16px; margin-bottom: 16px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 12px;">
                        <div>
                            <h4 style="font-size: 0.95rem; font-weight: 800; color: #0f172a; margin: 0;">
                                📸 1. Tentukan Opsi Image Generation Apa Saja yang Ingin Dibuat:
                            </h4>
                            <span style="font-size: 0.78rem; color: #64748b;">Pilih slot spesifik atau gunakan tombol preset cepat di kanan.</span>
                        </div>
                        <div style="display: flex; gap: 6px; flex-wrap: wrap;">
                            <button type="button" class="btn btn-sm" onclick="applySlotPreset('all')" style="background: #ecfdf5; border: 1px solid #a7f3d0; color: #047857; font-weight: 700; font-size: 0.72rem; padding: 4px 10px; border-radius: 6px;">
                                🌟 Semua 4 Slot (Lengkap)
                            </button>
                            <button type="button" class="btn btn-sm" onclick="applySlotPreset('hero_side')" style="background: #f0f9ff; border: 1px solid #bae6fd; color: #0369a1; font-weight: 700; font-size: 0.72rem; padding: 4px 10px; border-radius: 6px;">
                                📐 Hero & Side Saja
                            </button>
                            <button type="button" class="btn btn-sm" onclick="applySlotPreset('tread_usage')" style="background: #fffbeb; border: 1px solid #fde68a; color: #b45309; font-weight: 700; font-size: 0.72rem; padding: 4px 10px; border-radius: 6px;">
                                🔍 Tapak & Pemakaian
                            </button>
                        </div>
                    </div>

                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px;">
                        <!-- Slot 1 -->
                        <label class="gen-slot-option" style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; padding: 10px 12px; cursor: pointer; display: flex; gap: 10px; align-items: flex-start;">
                            <input type="checkbox" id="chkSlot1" checked style="width: 18px; height: 18px; accent-color: #059669; margin-top: 2px;">
                            <div>
                                <div style="font-weight: 800; font-size: 0.82rem; color: #059669;">Slot 1: Hero White BG</div>
                                <div style="font-size: 0.72rem; color: #64748b; margin-top: 2px; line-height: 1.3;">
                                    Tampak 3/4 studio e-commerce, latar putih murni #FFFFFF, rasio 1:1.
                                </div>
                            </div>
                        </label>

                        <!-- Slot 2 -->
                        <label class="gen-slot-option" style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; padding: 10px 12px; cursor: pointer; display: flex; gap: 10px; align-items: flex-start;">
                            <input type="checkbox" id="chkSlot2" checked style="width: 18px; height: 18px; accent-color: #0284c7; margin-top: 2px;">
                            <div>
                                <div style="font-weight: 800; font-size: 0.82rem; color: #0284c7;">Slot 2: 90° Lateral Profile</div>
                                <div style="font-size: 0.72rem; color: #64748b; margin-top: 2px; line-height: 1.3;">
                                    Tampak samping ortogonal melihat tinggi leher leher boot & kontur sol.
                                </div>
                            </div>
                        </label>

                        <!-- Slot 3 -->
                        <label class="gen-slot-option" style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; padding: 10px 12px; cursor: pointer; display: flex; gap: 10px; align-items: flex-start;">
                            <input type="checkbox" id="chkSlot3" checked style="width: 18px; height: 18px; accent-color: #d97706; margin-top: 2px;">
                            <div>
                                <div style="font-weight: 800; font-size: 0.82rem; color: #d97706;">Slot 3: Outsole Tread Detail</div>
                                <div style="font-size: 0.72rem; color: #64748b; margin-top: 2px; line-height: 1.3;">
                                    Tampilan tapak bawah sol dan alur cleat traksi anti-slip.
                                </div>
                            </div>
                        </label>

                        <!-- Slot 4 -->
                        <label class="gen-slot-option" style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; padding: 10px 12px; cursor: pointer; display: flex; gap: 10px; align-items: flex-start;">
                            <input type="checkbox" id="chkSlot4" checked style="width: 18px; height: 18px; accent-color: #7c3aed; margin-top: 2px;">
                            <div>
                                <div style="font-weight: 800; font-size: 0.82rem; color: #7c3aed;">Slot 4: Contextual In-Use</div>
                                <div style="font-size: 0.72rem; color: #64748b; margin-top: 2px; line-height: 1.3;">
                                    Foto penggunaan aktif di lapangan nyata (kebun/pabrik), framing kaki.
                                </div>
                            </div>
                        </label>
                    </div>
                </div>

                <!-- Section: Opsi Kualitas & Framing Kanvas -->
                <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px 16px; margin-bottom: 16px;">
                    <h4 style="font-size: 0.92rem; font-weight: 800; color: #0f172a; margin: 0 0 10px 0;">
                        📐 2. Pengaturan Resolusi Kanvas & Rasio Bingkai (Anti Kekecilan):
                    </h4>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px;">
                        <div>
                            <label style="font-size: 0.78rem; font-weight: 700; color: #475569; display: block; margin-bottom: 5px;">
                                Resolusi Kanvas (Rasio 1:1):
                            </label>
                            <select id="genOptSize" style="width: 100%; padding: 8px 10px; border: 1px solid #cbd5e1; border-radius: 6px; font-size: 0.82rem; font-weight: 600;">
                                <option value="1000" selected>1000 x 1000 px (Standar Photobank & E-Commerce)</option>
                                <option value="1200">1200 x 1200 px (Rekomendasi High-Res)</option>
                                <option value="1600">1600 x 1600 px (Alibaba HD Master)</option>
                            </select>
                        </div>
                        <div>
                            <label style="font-size: 0.78rem; font-weight: 700; color: #475569; display: block; margin-bottom: 5px;">
                                Rasio Isi Objek Sepatu:
                            </label>
                            <select id="genOptFill" style="width: 100%; padding: 8px 10px; border: 1px solid #cbd5e1; border-radius: 6px; font-size: 0.82rem; font-weight: 600;">
                                <option value="0.85" selected>85% Frame (Proporsional & Padat - Optimal)</option>
                                <option value="0.90">90% Frame (Penuh & Rapat)</option>
                                <option value="0.80">80% Frame (Longgar / Bernapas)</option>
                            </select>
                        </div>
                    </div>
                </div>

                <!-- Section: Target Lokasi Simpan -->
                <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px 16px; margin-bottom: 16px;">
                    <h4 style="font-size: 0.92rem; font-weight: 800; color: #0f172a; margin: 0 0 8px 0;">
                        📁 3. Target Penyimpanan Otomatis:
                    </h4>
                    <div style="display: flex; gap: 16px; flex-wrap: wrap; font-size: 0.8rem;">
                        <label style="display: flex; align-items: center; gap: 6px; cursor: pointer;">
                            <input type="checkbox" id="chkSaveShopee" checked style="accent-color: #059669;">
                            <span>Shopee_Product_Assets/[Folder]/</span>
                        </label>
                        <label style="display: flex; align-items: center; gap: 6px; cursor: pointer;">
                            <input type="checkbox" id="chkSaveFlow" checked style="accent-color: #059669;">
                            <span>Master Flow/</span>
                        </label>
                        <label style="display: flex; align-items: center; gap: 6px; cursor: pointer;">
                            <input type="checkbox" id="chkSavePhotobank" checked style="accent-color: #059669;">
                            <span>Output/Photobank_Siap_Upload/ & Manifest CSV</span>
                        </label>
                    </div>
                </div>

                <!-- Realtime Progress & Log Terminal -->
                <div style="background: #0f172a; border-radius: 10px; padding: 12px 16px; margin-bottom: 16px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <span style="font-size: 0.78rem; font-weight: 800; color: #38bdf8;">📡 Status & Realtime Terminal Logs:</span>
                        <span style="font-size: 0.72rem; color: #94a3b8;" id="genModalLogStatus">Siap Eksekusi</span>
                    </div>
                    <!-- Progress Bar -->
                    <div style="width: 100%; height: 8px; background: #334155; border-radius: 4px; overflow: hidden; margin-bottom: 8px;">
                        <div id="genModalProgressBar" style="width: 0%; height: 100%; background: linear-gradient(90deg, #10b981, #06b6d4); transition: width 0.3s ease;"></div>
                    </div>
                    <pre id="genModalLogBox" style="margin: 0; color: #a5f3fc; font-family: monospace; font-size: 0.74rem; max-height: 120px; overflow-y: auto; white-space: pre-wrap; word-break: break-all;">Pilih produk dan klik tombol 'Mulai Generate' untuk menjalankan proses native.</pre>
                </div>

                <!-- Action Button -->
                <div style="display: flex; justify-content: flex-end; gap: 10px;">
                    <button type="button" class="btn btn-secondary" onclick="closeModal('photobankGenModal')" style="padding: 10px 18px; border-radius: 8px; font-weight: 700;">
                        Batal
                    </button>
                    <button type="button" class="btn" id="btnExecuteGenModal" onclick="executeCustomPhotobankGeneration()" style="background: linear-gradient(135deg, #059669, #047857); color: #fff; font-weight: 800; font-size: 0.92rem; padding: 10px 24px; border-radius: 8px; box-shadow: 0 3px 10px rgba(5, 150, 105, 0.4);">
                        ⚡ Mulai Generate Foto (Native Standalone Engine)
                    </button>
                </div>
            </div>
        </div>
    </div>\n\n'''

    if target_modal_end in html and 'id="photobankGenModal"' not in html:
        html = html.replace(target_modal_end, new_gen_modal + target_modal_end, 1)
        print("1. Added #photobankGenModal successfully!")
    else:
        print("Notice: #photobankGenModal already present or target not found.")

    with open('App/template.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    main()
