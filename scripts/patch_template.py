# -*- coding: utf-8 -*-
"""
Patch App/template.html with Google Flow & Photobank Admin Studio Modal, Buttons, and JS.
"""
import sys

def main():
    with open('App/template.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Check if already patched
    if 'id="flowPhotobankModal"' in content:
        print("Already contains flowPhotobankModal")
        return

    # 2. Add #flowPhotobankModal after #shopeeJsonModal
    target_shopee_modal = '''                <pre id="shopeeJsonContent" style="background: #0f172a; color: #38bdf8; padding: 1.25rem; border-radius: 8px; font-size: 0.82rem; max-height: 550px; overflow-y: auto; font-family: monospace; white-space: pre-wrap; word-break: break-all;"></pre>
            </div>
        </div>
    </div>'''

    flow_modal_html = '''                <pre id="shopeeJsonContent" style="background: #0f172a; color: #38bdf8; padding: 1.25rem; border-radius: 8px; font-size: 0.82rem; max-height: 550px; overflow-y: auto; font-family: monospace; white-space: pre-wrap; word-break: break-all;"></pre>
            </div>
        </div>
    </div>

    <!-- MODAL 9: GOOGLE FLOW & PHOTOBANK ADMIN STUDIO -->
    <div class="modal-overlay" id="flowPhotobankModal">
        <div class="modal-content" style="max-width: 1100px; max-height: 92vh; display: flex; flex-direction: column;">
            <div class="modal-header" style="background: linear-gradient(135deg, #064e3b, #047857); color: #ffffff; padding: 1.1rem 1.5rem; border-top-left-radius: 12px; border-top-right-radius: 12px;">
                <div style="flex: 1;">
                    <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
                        <span style="font-size: 1.6rem;">⚡</span>
                        <h3 style="font-size: 1.25rem; font-weight: 800; color: #ffffff; margin: 0;" id="flowModalTitle">
                            Google Flow & Photobank Admin Studio (4-Slot Architecture)
                        </h3>
                        <span class="badge" id="flowModalCategoryBadge" style="background: #10b981; color: #ffffff; font-size: 0.75rem; padding: 3px 8px; border-radius: 6px;">
                            07_Classic_Boots
                        </span>
                    </div>
                    <div style="font-size: 0.8rem; color: #a7f3d0; margin-top: 6px; display: flex; gap: 16px; flex-wrap: wrap;">
                        <span>🎯 SKU: <strong id="flowModalSku" style="color: #fff;">SHP-001</strong></span>
                        <span>📦 Target: <a href="https://flow.google.com/project/5a88c3fd-477c-4eed-a126-f812ccfb079c" target="_blank" style="color: #6ee7b7; text-decoration: underline;">Google Flow (aufahots@gmail.com)</a></span>
                        <span>🌐 Server: <a href="https://admin.hotstrading.com/photo-bank" target="_blank" style="color: #6ee7b7; text-decoration: underline;">admin.hotstrading.com/photo-bank</a></span>
                    </div>
                </div>
                <button class="btn-close" style="color: #fff; opacity: 0.85;" onclick="closeModal('flowPhotobankModal')">&times;</button>
            </div>
            
            <div class="modal-body" style="padding: 1.25rem; overflow-y: auto; background: #f8fafc; flex: 1;">
                <!-- Control Action Bar -->
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; background: #ffffff; padding: 12px 16px; border-radius: 10px; border: 1px solid #e2e8f0; margin-bottom: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                    <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                        <button type="button" class="btn btn-sm" id="btnRunFlowGen" onclick="runFlowGenerationNow()" style="background: linear-gradient(135deg, #059669, #047857); color: #fff; font-weight: 800; border-radius: 6px; padding: 8px 14px; box-shadow: 0 2px 5px rgba(5, 150, 105, 0.3);">
                            ⚡ Generate 4 Variasi Slot
                        </button>
                        <button type="button" class="btn btn-sm" id="btnUploadAdminSim" onclick="uploadToPhotobankAdmin(true)" style="background: #0284c7; color: #fff; font-weight: 700; border-radius: 6px; padding: 8px 14px;">
                            🧪 Uji Coba Upload API (Simulasi)
                        </button>
                        <button type="button" class="btn btn-sm" id="btnUploadAdminReal" onclick="uploadToPhotobankAdmin(false)" style="background: #7c3aed; color: #fff; font-weight: 700; border-radius: 6px; padding: 8px 14px;">
                            🚀 Push API ke Admin Photobank
                        </button>
                    </div>
                    <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                        <button type="button" class="btn btn-sm" onclick="openPhotobankFolder()" style="background: #f1f5f9; border: 1px solid #cbd5e1; color: #334155; font-weight: 700; border-radius: 6px; padding: 8px 12px;">
                            📂 Buka Output Photobank
                        </button>
                        <button type="button" class="btn btn-sm" onclick="window.open('https://flow.google.com/project/5a88c3fd-477c-4eed-a126-f812ccfb079c', '_blank')" style="background: #eef2ff; border: 1px solid #c7d2fe; color: #4338ca; font-weight: 700; border-radius: 6px; padding: 8px 12px;">
                            🎨 Buka Google Flow Project
                        </button>
                    </div>
                </div>

                <!-- 4 Slots Visual Cards -->
                <div style="margin-bottom: 20px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <h4 style="font-size: 0.95rem; font-weight: 800; color: #1e293b; margin: 0;">
                            📸 4-Slot Standar Variasi Foto Produk (Alibaba & Photobank B2B)
                        </h4>
                        <span style="font-size: 0.78rem; color: #64748b;">Standar Rasio: 1:1 Square • Seamless Pure White (RGB 255,255,255) • Resolusi 1000px - 1600px</span>
                    </div>

                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 14px;" id="flowSlotsContainer">
                        <!-- Slot 1: Hero -->
                        <div class="flow-slot-card" style="background: #fff; border-radius: 10px; border: 1px solid #e2e8f0; padding: 12px; display: flex; flex-direction: column;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                <span style="font-size: 0.78rem; font-weight: 800; color: #059669; background: #ecfdf5; padding: 3px 8px; border-radius: 6px;">Slot 1: Hero White BG</span>
                                <span style="font-size: 0.7rem; color: #059669; font-weight: 700;" id="flowBadgeSlot1">✅ Ready</span>
                            </div>
                            <div style="width: 100%; aspect-ratio: 1/1; background: #f8fafc; border-radius: 8px; overflow: hidden; display: flex; align-items: center; justify-content: center; border: 1px solid #f1f5f9; margin-bottom: 8px;">
                                <img id="flowImgSlot1" src="" alt="Slot 1" style="width: 100%; height: 100%; object-fit: contain; cursor: pointer;" onclick="window.open(this.src)">
                            </div>
                            <div style="font-size: 0.72rem; font-family: monospace; color: #64748b; margin-bottom: 6px; word-break: break-all;" id="flowFileSlot1">-</div>
                            <div style="background: #0f172a; color: #94a3b8; padding: 8px; border-radius: 6px; font-size: 0.7rem; line-height: 1.35; flex: 1; max-height: 90px; overflow-y: auto; margin-bottom: 8px;" id="flowPromptSlot1">
                                Loading prompt...
                            </div>
                            <button type="button" class="btn btn-sm" onclick="copyFlowPrompt(1)" style="width: 100%; background: #f1f5f9; border: 1px solid #cbd5e1; font-size: 0.72rem; font-weight: 700; color: #334155; padding: 5px;">
                                📋 Copy Flow Prompt
                            </button>
                        </div>

                        <!-- Slot 2: Side Profile -->
                        <div class="flow-slot-card" style="background: #fff; border-radius: 10px; border: 1px solid #e2e8f0; padding: 12px; display: flex; flex-direction: column;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                <span style="font-size: 0.78rem; font-weight: 800; color: #0284c7; background: #f0f9ff; padding: 3px 8px; border-radius: 6px;">Slot 2: 90° Side Profile</span>
                                <span style="font-size: 0.7rem; color: #0284c7; font-weight: 700;" id="flowBadgeSlot2">✅ Ready</span>
                            </div>
                            <div style="width: 100%; aspect-ratio: 1/1; background: #f8fafc; border-radius: 8px; overflow: hidden; display: flex; align-items: center; justify-content: center; border: 1px solid #f1f5f9; margin-bottom: 8px;">
                                <img id="flowImgSlot2" src="" alt="Slot 2" style="width: 100%; height: 100%; object-fit: contain; cursor: pointer;" onclick="window.open(this.src)">
                            </div>
                            <div style="font-size: 0.72rem; font-family: monospace; color: #64748b; margin-bottom: 6px; word-break: break-all;" id="flowFileSlot2">-</div>
                            <div style="background: #0f172a; color: #94a3b8; padding: 8px; border-radius: 6px; font-size: 0.7rem; line-height: 1.35; flex: 1; max-height: 90px; overflow-y: auto; margin-bottom: 8px;" id="flowPromptSlot2">
                                Loading prompt...
                            </div>
                            <button type="button" class="btn btn-sm" onclick="copyFlowPrompt(2)" style="width: 100%; background: #f1f5f9; border: 1px solid #cbd5e1; font-size: 0.72rem; font-weight: 700; color: #334155; padding: 5px;">
                                📋 Copy Flow Prompt
                            </button>
                        </div>

                        <!-- Slot 3: Outsole Tread -->
                        <div class="flow-slot-card" style="background: #fff; border-radius: 10px; border: 1px solid #e2e8f0; padding: 12px; display: flex; flex-direction: column;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                <span style="font-size: 0.78rem; font-weight: 800; color: #d97706; background: #fffbeb; padding: 3px 8px; border-radius: 6px;">Slot 3: Outsole Tread Cleats</span>
                                <span style="font-size: 0.7rem; color: #d97706; font-weight: 700;" id="flowBadgeSlot3">✅ Ready</span>
                            </div>
                            <div style="width: 100%; aspect-ratio: 1/1; background: #f8fafc; border-radius: 8px; overflow: hidden; display: flex; align-items: center; justify-content: center; border: 1px solid #f1f5f9; margin-bottom: 8px;">
                                <img id="flowImgSlot3" src="" alt="Slot 3" style="width: 100%; height: 100%; object-fit: contain; cursor: pointer;" onclick="window.open(this.src)">
                            </div>
                            <div style="font-size: 0.72rem; font-family: monospace; color: #64748b; margin-bottom: 6px; word-break: break-all;" id="flowFileSlot3">-</div>
                            <div style="background: #0f172a; color: #94a3b8; padding: 8px; border-radius: 6px; font-size: 0.7rem; line-height: 1.35; flex: 1; max-height: 90px; overflow-y: auto; margin-bottom: 8px;" id="flowPromptSlot3">
                                Loading prompt...
                            </div>
                            <button type="button" class="btn btn-sm" onclick="copyFlowPrompt(3)" style="width: 100%; background: #f1f5f9; border: 1px solid #cbd5e1; font-size: 0.72rem; font-weight: 700; color: #334155; padding: 5px;">
                                📋 Copy Flow Prompt
                            </button>
                        </div>

                        <!-- Slot 4: Contextual In-Use -->
                        <div class="flow-slot-card" style="background: #fff; border-radius: 10px; border: 1px solid #e2e8f0; padding: 12px; display: flex; flex-direction: column;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                <span style="font-size: 0.78rem; font-weight: 800; color: #7c3aed; background: #f5f3ff; padding: 3px 8px; border-radius: 6px;">Slot 4: Contextual In-Use</span>
                                <span style="font-size: 0.7rem; color: #7c3aed; font-weight: 700;" id="flowBadgeSlot4">✅ Ready</span>
                            </div>
                            <div style="width: 100%; aspect-ratio: 1/1; background: #f8fafc; border-radius: 8px; overflow: hidden; display: flex; align-items: center; justify-content: center; border: 1px solid #f1f5f9; margin-bottom: 8px;">
                                <img id="flowImgSlot4" src="" alt="Slot 4" style="width: 100%; height: 100%; object-fit: contain; cursor: pointer;" onclick="window.open(this.src)">
                            </div>
                            <div style="font-size: 0.72rem; font-family: monospace; color: #64748b; margin-bottom: 6px; word-break: break-all;" id="flowFileSlot4">-</div>
                            <div style="background: #0f172a; color: #94a3b8; padding: 8px; border-radius: 6px; font-size: 0.7rem; line-height: 1.35; flex: 1; max-height: 90px; overflow-y: auto; margin-bottom: 8px;" id="flowPromptSlot4">
                                Loading prompt...
                            </div>
                            <button type="button" class="btn btn-sm" onclick="copyFlowPrompt(4)" style="width: 100%; background: #f1f5f9; border: 1px solid #cbd5e1; font-size: 0.72rem; font-weight: 700; color: #334155; padding: 5px;">
                                📋 Copy Flow Prompt
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Photobank Status & Categories Breakdown -->
                <div style="background: #ffffff; padding: 14px 16px; border-radius: 10px; border: 1px solid #e2e8f0; margin-bottom: 16px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 12px;">
                        <h4 style="font-size: 0.92rem; font-weight: 800; color: #0f172a; margin: 0;">
                            📊 Status Photobank Server & 11 Kategori Resmi (admin.hotstrading.com)
                        </h4>
                        <span id="photobankTotalBadge" style="font-size: 0.8rem; font-weight: 800; color: #059669; background: #d1fae5; padding: 3px 10px; border-radius: 20px;">
                            Total: 421 Foto Siap Upload
                        </span>
                    </div>
                    <div id="photobankCategoriesList" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 8px; font-size: 0.75rem;">
                        <!-- Categories dynamically loaded -->
                    </div>
                </div>

                <!-- API Logs / Result Box -->
                <div style="background: #0f172a; padding: 12px 16px; border-radius: 8px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <span style="font-size: 0.76rem; font-weight: 800; color: #38bdf8;">📡 API Response & Sync Payload:</span>
                        <span style="font-size: 0.7rem; color: #94a3b8;" id="flowApiStatus">Idle</span>
                    </div>
                    <pre id="flowApiLogBox" style="margin: 0; color: #a5f3fc; font-family: monospace; font-size: 0.74rem; max-height: 140px; overflow-y: auto; white-space: pre-wrap; word-break: break-all;">Ready for testing sample generation or upload API.</pre>
                </div>
            </div>
        </div>
    </div>'''

    if target_shopee_modal in content:
        content = content.replace(target_shopee_modal, flow_modal_html, 1)
        print("1. Added flowPhotobankModal successfully.")
    else:
        print("ERROR: Target for modal not found!")
        sys.exit(1)

    # 3. Add header button to Shopee Studio
    target_header_btn = '''<button type="button" class="btn btn-sm" onclick="openShopeeFolder('')" style="background: #0f172a; color: #fff; font-weight: 700; border-radius: 8px; padding: 8px 14px; box-shadow: 0 2px 6px rgba(15,23,42,0.2);">
                                📂 Buka Folder Root Assets
                            </button>'''

    new_header_btn = '''<button type="button" class="btn btn-sm" onclick="openPhotobankOverviewModal()" style="background: linear-gradient(135deg, #10b981, #059669); color: #fff; font-weight: 800; border-radius: 8px; padding: 8px 16px; box-shadow: 0 3px 8px rgba(16, 185, 129, 0.35);">
                                ⚡ Flow & Photobank Admin Studio
                            </button>
                            <button type="button" class="btn btn-sm" onclick="openShopeeFolder('')" style="background: #0f172a; color: #fff; font-weight: 700; border-radius: 8px; padding: 8px 14px; box-shadow: 0 2px 6px rgba(15,23,42,0.2);">
                                📂 Buka Folder Root Assets
                            </button>'''

    if target_header_btn in content:
        content = content.replace(target_header_btn, new_header_btn, 1)
        print("2. Added header button to Shopee Studio successfully.")
    else:
        print("ERROR: Target for header button not found!")
        sys.exit(1)

    # 4. Add action button to Shopee Card
    target_card_btn = '''<!-- Action Buttons -->
                        <div class="shopee-actions-row">
                            <button type="button" class="btn btn-sm" onclick="openShopeeJsonModal('${p.folder_name}', '${p.product_name.replace(/'/g, "\\\\'")}')" style="flex: 1; background: #f8fafc; border: 1px solid var(--border); color: #0f172a; font-weight: 700; font-size: 0.76rem; border-radius: 6px; padding: 7px 10px;">
                                📄 View Alibaba JSON
                            </button>'''

    new_card_btn = '''<!-- Action Buttons -->
                        <div class="shopee-actions-row">
                            <button type="button" class="btn btn-sm" onclick="openFlowModal('${p.sku}', '${p.folder_name}', '${p.product_name.replace(/'/g, "\\\\'")}')" style="background: linear-gradient(135deg, #059669, #047857); color: #fff; font-weight: 700; font-size: 0.76rem; border-radius: 6px; padding: 7px 10px;" title="Google Flow 4-Slot Studio & Photobank Upload">
                                ⚡ Flow & Photobank
                            </button>
                            <button type="button" class="btn btn-sm" onclick="openShopeeJsonModal('${p.folder_name}', '${p.product_name.replace(/'/g, "\\\\'")}')" style="flex: 1; background: #f8fafc; border: 1px solid var(--border); color: #0f172a; font-weight: 700; font-size: 0.76rem; border-radius: 6px; padding: 7px 10px;">
                                📄 View Alibaba JSON
                            </button>'''

    if target_card_btn in content:
        content = content.replace(target_card_btn, new_card_btn, 1)
        print("3. Added card action button successfully.")
    else:
        print("ERROR: Target for card button not found!")
        sys.exit(1)

    # 5. Add JavaScript functions before </script>
    target_end_script = '''    </script>
</body>
</html>'''

    flow_js_code = '''        // Google Flow & Photobank Admin Studio Logic
        let currentFlowSku = 'SHP-001';
        let currentFlowFolder = 'AP_Boots_XTR_Hitam_Sepatu_Boot_PVC';
        let currentFlowProductName = 'AP Boots XTR Hitam Sepatu Boot PVC';
        let currentFlowCategoryFolder = '07_Classic_Boots';
        let flowPromptsCache = {};

        async function openPhotobankOverviewModal() {
            openFlowModal('SHP-001', 'AP_Boots_XTR_Hitam_Sepatu_Boot_PVC', 'AP Boots XTR Hitam Sepatu Boot PVC');
        }

        async function openFlowModal(sku, folder, productName) {
            currentFlowSku = sku || 'SHP-001';
            currentFlowFolder = folder || 'AP_Boots_XTR_Hitam_Sepatu_Boot_PVC';
            currentFlowProductName = productName || folder.replace(/_/g, ' ');

            document.getElementById('flowModalTitle').innerText = `Flow & Photobank Studio: ${currentFlowProductName}`;
            document.getElementById('flowModalSku').innerText = currentFlowSku;
            document.getElementById('flowPhotobankModal').classList.add('active');

            refreshFlowSlotsDisplay();
            loadPhotobankOverviewStatus();
        }

        async function refreshFlowSlotsDisplay() {
            const folder = currentFlowFolder;
            const sku = currentFlowSku;
            const cleanSku = sku.replace(/-/g, '_');
            const baseName = `${cleanSku}_${folder.substring(0, 25)}`;

            const p1 = `Using the attached reference photos, create a professional e-commerce commercial studio product photograph of ${currentFlowProductName}. Front 3/4 angle, standing upright, centered, occupying 85% frame. Seamless pure white background (RGB 255,255,255), soft even studio lighting, subtle contact shadow. 8k clarity, square 1:1 ratio, no text.`;
            const p2 = `Using the attached reference photos, create a clean e-commerce commercial product photograph of ${currentFlowProductName} from a straight orthogonal 90-degree lateral side profile view. Highlighting boot shaft height, waterproof seamless contour, and sole thickness. Seamless pure white background (RGB 255,255,255), square 1:1 ratio, no text.`;
            const p3 = `Using the attached reference photos, create a high-definition commercial product photo of ${currentFlowProductName} showcasing the bottom outsole tread pattern and anti-slip traction lugs. Pure white background (RGB 255,255,255), square 1:1 ratio, sharp focus.`;
            const p4 = `Using the attached reference photos, create a realistic photograph of ${currentFlowProductName} being actively worn on wet agricultural plantation terrain and muddy ground in outdoor daylight. Lower-body framing from knees down, no visible human faces, square 1:1 ratio, photorealistic.`;

            flowPromptsCache = { 1: p1, 2: p2, 3: p3, 4: p4 };

            document.getElementById('flowPromptSlot1').innerText = p1;
            document.getElementById('flowPromptSlot2').innerText = p2;
            document.getElementById('flowPromptSlot3').innerText = p3;
            document.getElementById('flowPromptSlot4').innerText = p4;

            document.getElementById('flowFileSlot1').innerText = `${baseName}_slot_1_hero.webp`;
            document.getElementById('flowFileSlot2').innerText = `${baseName}_slot_2_side.webp`;
            document.getElementById('flowFileSlot3').innerText = `${baseName}_slot_3_tread.webp`;
            document.getElementById('flowFileSlot4').innerText = `${baseName}_slot_4_usage.webp`;

            const t = Date.now();
            document.getElementById('flowImgSlot1').src = `/shopee-assets/${encodeURIComponent(folder)}/hero_${encodeURIComponent(folder)}.webp?t=${t}`;
            document.getElementById('flowImgSlot2').src = `/shopee-assets/${encodeURIComponent(folder)}/side_${encodeURIComponent(folder)}.webp?t=${t}`;
            document.getElementById('flowImgSlot3').src = `/shopee-assets/${encodeURIComponent(folder)}/tread_${encodeURIComponent(folder)}.webp?t=${t}`;
            document.getElementById('flowImgSlot4').src = `/shopee-assets/${encodeURIComponent(folder)}/usage_${encodeURIComponent(folder)}.webp?t=${t}`;

            try {
                const res = await fetch(`/api/shopee/product-json?folder=${encodeURIComponent(folder)}`);
                const jData = await res.json();
                if (jData.success && jData.data && jData.data.google_flow_and_photobank_slots) {
                    const slots = jData.data.google_flow_and_photobank_slots.slots_generated || {};
                    if (slots.slot_1_hero) {
                        flowPromptsCache[1] = slots.slot_1_hero.prompt;
                        document.getElementById('flowPromptSlot1').innerText = slots.slot_1_hero.prompt;
                    }
                    if (slots.slot_2_side) {
                        flowPromptsCache[2] = slots.slot_2_side.prompt;
                        document.getElementById('flowPromptSlot2').innerText = slots.slot_2_side.prompt;
                    }
                    if (slots.slot_3_tread) {
                        flowPromptsCache[3] = slots.slot_3_tread.prompt;
                        document.getElementById('flowPromptSlot3').innerText = slots.slot_3_tread.prompt;
                    }
                    if (slots.slot_4_usage) {
                        flowPromptsCache[4] = slots.slot_4_usage.prompt;
                        document.getElementById('flowPromptSlot4').innerText = slots.slot_4_usage.prompt;
                    }
                    if (jData.data.google_flow_and_photobank_slots.photobank_ready) {
                        const cat = jData.data.google_flow_and_photobank_slots.photobank_ready.category_folder;
                        currentFlowCategoryFolder = cat;
                        document.getElementById('flowModalCategoryBadge').innerText = cat;
                    }
                }
            } catch (e) {
                console.warn('Could not read product json slots', e);
            }
        }

        async function loadPhotobankOverviewStatus() {
            try {
                const res = await fetch('/api/photobank/status');
                const data = await res.json();
                if (data.success) {
                    document.getElementById('photobankTotalBadge').innerText = `Total: ${data.total_photobank_files} Foto Siap Upload (${data.manifest_entries} Manifest)`;
                    const catContainer = document.getElementById('photobankCategoriesList');
                    let catHtml = '';
                    for (const [folder, info] of Object.entries(data.categories)) {
                        catHtml += `
                            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 6px 8px;">
                                <div style="font-weight: 700; color: #1e293b; display: flex; justify-content: space-between;">
                                    <span>${folder.substring(0, 15)}...</span>
                                    <span style="color: #059669; font-weight: 800;">${info.count}</span>
                                </div>
                                <div style="color: #64748b; font-size: 0.68rem;">${info.group_name}</div>
                            </div>
                        `;
                    }
                    catContainer.innerHTML = catHtml;
                }
            } catch (e) {
                console.error(e);
            }
        }

        async function runFlowGenerationNow() {
            const btn = document.getElementById('btnRunFlowGen');
            btn.disabled = true;
            btn.innerHTML = '⏳ Menjalankan Generator 4 Slot...';
            document.getElementById('flowApiStatus').innerText = 'Generating...';

            try {
                const res = await fetch('/api/photobank/generate-sample', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({sku: currentFlowSku, folder: currentFlowFolder})
                });
                const data = await res.json();
                document.getElementById('flowApiLogBox').innerText = JSON.stringify(data, null, 2);
                if (data.success) {
                    document.getElementById('flowApiStatus').innerText = '✅ Generation Success';
                    showToast(`✅ Berhasil generate 4 slot untuk ${currentFlowSku}!`);
                    refreshFlowSlotsDisplay();
                    loadPhotobankOverviewStatus();
                } else {
                    document.getElementById('flowApiStatus').innerText = '❌ Error';
                    alert('Gagal generate: ' + data.error);
                }
            } catch (e) {
                document.getElementById('flowApiStatus').innerText = '❌ Network Error';
                alert('Network Error: ' + e);
            } finally {
                btn.disabled = false;
                btn.innerHTML = '⚡ Generate 4 Variasi Slot';
            }
        }

        async function uploadToPhotobankAdmin(simulate = true) {
            const btn = simulate ? document.getElementById('btnUploadAdminSim') : document.getElementById('btnUploadAdminReal');
            const orig = btn.innerHTML;
            btn.disabled = true;
            btn.innerHTML = '⏳ Processing API...';
            document.getElementById('flowApiStatus').innerText = simulate ? 'Simulating Upload...' : 'Uploading API...';

            try {
                const res = await fetch('/api/photobank/upload-admin', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        sku: currentFlowSku,
                        folder: currentFlowFolder,
                        simulate: simulate
                    })
                });
                const data = await res.json();
                document.getElementById('flowApiLogBox').innerText = JSON.stringify(data, null, 2);
                if (data.success) {
                    document.getElementById('flowApiStatus').innerText = simulate ? '✅ Simulation Passed (4/4 slots)' : '✅ Upload Done';
                    showToast(simulate ? '🧪 Uji coba simulasi API Photobank sukses!' : '🚀 Berhasil upload ke Admin Photobank!');
                } else {
                    document.getElementById('flowApiStatus').innerText = '❌ Upload Failed';
                    alert('Error: ' + data.error);
                }
            } catch (e) {
                document.getElementById('flowApiStatus').innerText = '❌ Network Error';
                alert('Network Error: ' + e);
            } finally {
                btn.disabled = false;
                btn.innerHTML = orig;
            }
        }

        async function openPhotobankFolder() {
            try {
                const res = await fetch('/api/photobank/open-folder');
                const data = await res.json();
                if (data.success) {
                    showToast('📂 Membuka folder Photobank di Windows Explorer...');
                } else {
                    alert('Gagal: ' + data.error);
                }
            } catch (e) {
                alert('Error: ' + e);
            }
        }

        function copyFlowPrompt(slotNum) {
            const prompt = flowPromptsCache[slotNum] || '';
            if (!prompt) return;
            navigator.clipboard.writeText(prompt).then(() => {
                showToast(`📋 Prompt Slot ${slotNum} disalin ke clipboard!`);
            }).catch(e => {
                showToast('❌ Gagal menyalin prompt');
            });
        }
    </script>
</body>
</html>'''

    if target_end_script in content:
        content = content.replace(target_end_script, flow_js_code, 1)
        print("4. Added Flow JavaScript logic successfully.")
    else:
        print("ERROR: Target for end script not found!")
        sys.exit(1)

    with open('App/template.html', 'w', encoding='utf-8') as f:
        f.write(content)

    print("ALL PATCHES APPLIED TO App/template.html SUCCESSFULLY!")

if __name__ == '__main__':
    main()
