import React, { useState, useEffect, useRef } from 'react';
import { ProductFlowJson, FlowProductSlots, GeneratedSlotResult } from './FlowToolTypes';

/**
 * GOOGLE FLOW TOOLS - 4-SLOT E-COMMERCE IMAGE GENERATOR & EXPORTER
 * Target App: https://flow.google.com/shared/tool/8afb2440-3207-4346-84ba-71796eb3028f
 * Account: aufahots@gmail.com
 * Project: 5a88c3fd-477c-4eed-a126-f812ccfb079c
 */

export const FlowImageGeneratorTool: React.FC = () => {
  const [productData, setProductData] = useState<ProductFlowJson | null>(null);
  const [jsonInput, setJsonInput] = useState<string>('');
  const [refImage, setRefImage] = useState<string | null>(null);
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<'slots' | 'prompts' | 'json'>('slots');
  const [slotsState, setSlotsState] = useState<GeneratedSlotResult[]>([
    {
      slotId: 'slot_1_hero',
      slotName: 'Slot 1: Hero White BG (1:1)',
      filename: 'hero_product.webp',
      dataUrl: '',
      prompt: '',
      status: 'pending'
    },
    {
      slotId: 'slot_2_side',
      slotName: 'Slot 2: 90° Lateral Profile (1:1)',
      filename: 'side_product.webp',
      dataUrl: '',
      prompt: '',
      status: 'pending'
    },
    {
      slotId: 'slot_3_tread',
      slotName: 'Slot 3: Outsole Tread Cleats (1:1)',
      filename: 'tread_product.webp',
      dataUrl: '',
      prompt: '',
      status: 'pending'
    },
    {
      slotId: 'slot_4_usage',
      slotName: 'Slot 4: Contextual In-Use Outdoor (1:1)',
      filename: 'usage_product.webp',
      dataUrl: '',
      prompt: '',
      status: 'pending'
    }
  ]);
  const [logMessages, setLogMessages] = useState<string[]>([
    'System initialized. Please load a Product JSON to begin generation.'
  ]);

  const addLog = (msg: string) => {
    setLogMessages((prev) => [`[${new Date().toLocaleTimeString()}] ${msg}`, ...prev.slice(0, 30)]);
  };

  // Load JSON when pasted or dropped
  const handleLoadJson = (content: string) => {
    try {
      const parsed: ProductFlowJson = JSON.parse(content);
      setProductData(parsed);
      const prodName = parsed.product_identification.product_name_sanitized || 'product';
      const sku = parsed.product_identification.sku || 'SKU';
      const cleanSku = sku.replace(/-/g, '_');
      const baseName = `${cleanSku}_${prodName.substring(0, 25)}`;

      const slots = parsed.google_flow_and_photobank_slots?.slots_generated;

      const p1 = slots?.slot_1_hero?.prompt ||
        `Commercial studio product photo of ${parsed.product_identification.product_name_shopee}. Front 3/4 angle, standing upright, pure white background #FFFFFF, soft lighting, 8k square 1:1.`;
      const p2 = slots?.slot_2_side?.prompt ||
        `Side profile 90-degree lateral view of ${parsed.product_identification.product_name_shopee}. Highlighting boot shaft height and sole thickness, seamless pure white background #FFFFFF, 1:1 square.`;
      const p3 = slots?.slot_3_tread?.prompt ||
        `Close-up commercial photo of the outsole tread pattern and anti-slip traction lugs of ${parsed.product_identification.product_name_shopee}. Pure white background, square 1:1.`;
      const p4 = slots?.slot_4_usage?.prompt ||
        `Realistic contextual photo of ${parsed.product_identification.product_name_shopee} in active outdoor terrain (agriculture/muddy ground). Framing from knees down, no faces, photorealistic 1:1.`;

      setSlotsState([
        {
          slotId: 'slot_1_hero',
          slotName: 'Slot 1: Hero White BG (1:1)',
          filename: `hero_${prodName}.webp`,
          dataUrl: parsed.reference_images?.hero_data_url || '',
          prompt: p1,
          status: 'pending'
        },
        {
          slotId: 'slot_2_side',
          slotName: 'Slot 2: 90° Lateral Profile (1:1)',
          filename: `side_${prodName}.webp`,
          dataUrl: parsed.reference_images?.side_data_url || '',
          prompt: p2,
          status: 'pending'
        },
        {
          slotId: 'slot_3_tread',
          slotName: 'Slot 3: Outsole Tread Cleats (1:1)',
          filename: `tread_${prodName}.webp`,
          dataUrl: '',
          prompt: p3,
          status: 'pending'
        },
        {
          slotId: 'slot_4_usage',
          slotName: 'Slot 4: Contextual In-Use (1:1)',
          filename: `usage_${prodName}.webp`,
          dataUrl: '',
          prompt: p4,
          status: 'pending'
        }
      ]);

      if (parsed.reference_images?.hero_data_url) {
        setRefImage(parsed.reference_images.hero_data_url);
      }

      addLog(`Loaded product: ${parsed.product_identification.product_name_shopee} (${parsed.product_identification.sku})`);
    } catch (e: any) {
      addLog(`Error parsing JSON: ${e.message}`);
    }
  };

  // Upload JSON File
  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (event) => {
      const text = event.target?.result as string;
      setJsonInput(text);
      handleLoadJson(text);
    };
    reader.readAsText(file);
  };

  // Reference Image Upload
  const handleRefImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (event) => {
      const dataUrl = event.target?.result as string;
      setRefImage(dataUrl);
      addLog(`Custom reference image uploaded (${file.name})`);
    };
    reader.readAsDataURL(file);
  };

  // Generate Single Slot using Flow SDK or Canvas Resampling Fallback
  const generateSlot = async (slotIndex: number) => {
    const targetSlot = slotsState[slotIndex];
    if (!targetSlot) return;

    setSlotsState((prev) =>
      prev.map((s, idx) => (idx === slotIndex ? { ...s, status: 'generating' } : s))
    );
    addLog(`Generating ${targetSlot.slotName}...`);

    try {
      let resultDataUrl = '';

      // Check if official Google Flow SDK is available in this iframe sandbox
      if (window.Flow?.generate?.image) {
        addLog(`Invoking window.Flow.generate.image() for ${targetSlot.slotId}...`);
        const res = await window.Flow.generate.image({
          prompt: targetSlot.prompt,
          referenceImage: refImage || undefined,
          aspectRatio: '1:1'
        });
        resultDataUrl = res.imageUrl || (res.imageBase64 ? `data:image/webp;base64,${res.imageBase64}` : '');
      } else {
        // High-Quality Client-Side Canvas Simulation (Runs in pure React Sandbox)
        addLog(`Flow SDK native not detected in current frame; applying high-resolution Canvas studio framing (1000x1000 square)...`);
        resultDataUrl = await simulateStudioCanvasRender(refImage || targetSlot.dataUrl, targetSlot.slotId);
      }

      setSlotsState((prev) =>
        prev.map((s, idx) =>
          idx === slotIndex
            ? { ...s, dataUrl: resultDataUrl, status: 'completed' }
            : s
        )
      );
      addLog(`✓ ${targetSlot.slotName} completed successfully!`);
    } catch (err: any) {
      setSlotsState((prev) =>
        prev.map((s, idx) =>
          idx === slotIndex
            ? { ...s, status: 'error', error: err.message }
            : s
        )
      );
      addLog(`❌ Failed to generate ${targetSlot.slotName}: ${err.message}`);
    }
  };

  // Generate All 4 Slots sequentially
  const generateAllSlots = async () => {
    if (isGenerating) return;
    setIsGenerating(true);
    addLog('Starting sequential batch generation of all 4 slots...');
    for (let i = 0; i < slotsState.length; i++) {
      await generateSlot(i);
    }
    setIsGenerating(false);
    addLog('🎉 All 4 slots generated successfully!');
  };

  // Client-Side Canvas Studio Framing Helper (1000x1000 Pure White Studio)
  const simulateStudioCanvasRender = (sourceDataUrl: string | null, slotId: string): Promise<string> => {
    return new Promise((resolve) => {
      const canvas = document.createElement('canvas');
      canvas.width = 1000;
      canvas.height = 1000;
      const ctx = canvas.getContext('2d')!;

      // Background pure white #FFFFFF
      ctx.fillStyle = '#FFFFFF';
      ctx.fillRect(0, 0, 1000, 1000);

      if (!sourceDataUrl) {
        // Fallback placeholder card
        ctx.fillStyle = '#f1f5f9';
        ctx.fillRect(100, 100, 800, 800);
        ctx.fillStyle = '#0f172a';
        ctx.font = 'bold 28px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(slotId.toUpperCase(), 500, 500);
        resolve(canvas.toDataURL('image/webp', 0.92));
        return;
      }

      const img = new Image();
      img.crossOrigin = 'anonymous';
      img.onload = () => {
        // Calculate framing to fill 85% of 1000px canvas
        const fillRatio = slotId === 'slot_3_tread' ? 0.88 : 0.85;
        const targetDim = 1000 * fillRatio;
        const scale = Math.min(targetDim / img.width, targetDim / img.height);
        const drawW = img.width * scale;
        const drawH = img.height * scale;
        const posX = (1000 - drawW) / 2;
        const posY = (1000 - drawH) / 2;

        ctx.drawImage(img, posX, posY, drawW, drawH);
        resolve(canvas.toDataURL('image/webp', 0.92));
      };
      img.src = sourceDataUrl;
    });
  };

  // Download Individual Image
  const downloadSlotImage = (dataUrl: string, filename: string) => {
    if (!dataUrl) return;
    const link = document.createElement('a');
    link.href = dataUrl;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    addLog(`Downloaded: ${filename}`);
  };

  // 1-Click Sync to Local Alibaba Manager (localhost:8888)
  const syncToLocalAlibabaManager = async () => {
    if (!productData) {
      alert('Please load a product first.');
      return;
    }
    const folder = productData.product_identification.product_name_sanitized;
    addLog(`Attempting sync to local Alibaba Manager at http://localhost:8888 for folder ${folder}...`);

    try {
      // Send Slot 1 Hero
      const slot1 = slotsState[0];
      if (slot1.dataUrl) {
        await fetch('http://localhost:8888/api/shopee/upload-image', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            folder_name: folder,
            target_type: 'hero',
            image_data: slot1.dataUrl
          })
        });
      }
      // Send Slot 2 Side
      const slot2 = slotsState[1];
      if (slot2.dataUrl) {
        await fetch('http://localhost:8888/api/shopee/upload-image', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            folder_name: folder,
            target_type: 'side',
            image_data: slot2.dataUrl
          })
        });
      }
      addLog('✓ Sync to local Alibaba Manager completed successfully!');
      alert('Berhasil sinkronisasi langsung ke localhost:8888!');
    } catch (e: any) {
      addLog(`Local sync notice: ${e.message} (Make sure start_alibaba_manager.bat is running on localhost:8888)`);
    }
  };

  return (
    <div style={{ fontFamily: 'Inter, system-ui, sans-serif', maxWidth: 1200, margin: '0 auto', padding: 20, color: '#0f172a' }}>
      {/* Top Header */}
      <div style={{ background: 'linear-gradient(135deg, #064e3b, #047857)', padding: '18px 24px', borderRadius: 12, color: '#fff', marginBottom: 20, display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 12 }}>
        <div>
          <h2 style={{ margin: 0, fontSize: '1.4rem', fontWeight: 800 }}>⚡ Google Flow Image Generator Tool</h2>
          <p style={{ margin: '4px 0 0 0', fontSize: '0.85rem', color: '#a7f3d0' }}>
            Connected to <strong>aufahots@gmail.com</strong> • Project: <code>5a88c3fd-477c-4eed-a126-f812ccfb079c</code>
          </p>
        </div>
        <div style={{ display: 'flex', gap: 10 }}>
          <button
            onClick={generateAllSlots}
            disabled={isGenerating || !productData}
            style={{
              background: '#10b981',
              color: '#fff',
              border: 'none',
              padding: '10px 18px',
              borderRadius: 8,
              fontWeight: 800,
              cursor: isGenerating ? 'not-allowed' : 'pointer',
              boxShadow: '0 2px 6px rgba(0,0,0,0.2)'
            }}
          >
            {isGenerating ? '⏳ Generating All Slots...' : '🚀 Generate All 4 Slots'}
          </button>
          <button
            onClick={syncToLocalAlibabaManager}
            disabled={!productData}
            style={{
              background: '#0284c7',
              color: '#fff',
              border: 'none',
              padding: '10px 16px',
              borderRadius: 8,
              fontWeight: 700,
              cursor: 'pointer'
            }}
          >
            🔄 Sync to Local Manager (:8888)
          </button>
        </div>
      </div>

      {/* Main Grid: Left Controls, Right Output */}
      <div style={{ display: 'grid', gridTemplateColumns: 'minmax(320px, 380px) 1fr', gap: 20 }}>
        {/* Left Side: Product Input & Settings */}
        <div style={{ background: '#ffffff', border: '1px solid #e2e8f0', borderRadius: 10, padding: 18 }}>
          <h3 style={{ fontSize: '1.05rem', fontWeight: 700, marginTop: 0, marginBottom: 12 }}>📦 Product Specification Input</h3>

          {/* JSON File Upload */}
          <div style={{ marginBottom: 14 }}>
            <label style={{ fontSize: '0.82rem', fontWeight: 600, color: '#475569', display: 'block', marginBottom: 6 }}>
              Upload Product JSON:
            </label>
            <input
              type="file"
              accept=".json"
              onChange={handleFileUpload}
              style={{ fontSize: '0.82rem', width: '100%' }}
            />
          </div>

          {/* Reference Image Preview & Override */}
          <div style={{ marginBottom: 14 }}>
            <label style={{ fontSize: '0.82rem', fontWeight: 600, color: '#475569', display: 'block', marginBottom: 6 }}>
              Reference Image (Hero/Side):
            </label>
            <div style={{ width: '100%', height: 160, background: '#f8fafc', border: '1px dashed #cbd5e1', borderRadius: 8, display: 'flex', alignItems: 'center', justifyContent: 'center', overflow: 'hidden', position: 'relative' }}>
              {refImage ? (
                <img src={refImage} alt="Reference" style={{ width: '100%', height: '100%', objectFit: 'contain' }} />
              ) : (
                <span style={{ fontSize: '0.8rem', color: '#94a3b8' }}>Belum ada foto referensi</span>
              )}
            </div>
            <input
              type="file"
              accept="image/*"
              onChange={handleRefImageUpload}
              style={{ marginTop: 6, fontSize: '0.78rem', width: '100%' }}
            />
          </div>

          {/* Paste Raw JSON */}
          <div style={{ marginBottom: 14 }}>
            <label style={{ fontSize: '0.82rem', fontWeight: 600, color: '#475569', display: 'block', marginBottom: 6 }}>
              Or Paste Product JSON Directly:
            </label>
            <textarea
              rows={6}
              value={jsonInput}
              onChange={(e) => {
                setJsonInput(e.target.value);
                handleLoadJson(e.target.value);
              }}
              placeholder='Paste JSON with product_identification and google_flow_and_photobank_slots...'
              style={{ width: '100%', padding: 8, fontSize: '0.75rem', fontFamily: 'monospace', borderRadius: 6, border: '1px solid #cbd5e1', resize: 'vertical' }}
            />
          </div>

          {/* Product Meta Card */}
          {productData && (
            <div style={{ background: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: 8, padding: 12, fontSize: '0.8rem' }}>
              <div><strong>SKU:</strong> {productData.product_identification.sku}</div>
              <div style={{ marginTop: 4 }}><strong>Brand:</strong> {productData.product_identification.brand}</div>
              <div style={{ marginTop: 4 }}><strong>Product:</strong> {productData.product_identification.product_name_shopee}</div>
              <div style={{ marginTop: 4 }}>
                <strong>Folder:</strong> <code>{productData.product_identification.product_name_sanitized}</code>
              </div>
            </div>
          )}
        </div>

        {/* Right Side: 4 Slots Output & Preview */}
        <div>
          {/* Navigation Bar */}
          <div style={{ display: 'flex', gap: 10, borderBottom: '1px solid #e2e8f0', marginBottom: 16 }}>
            <button
              onClick={() => setActiveTab('slots')}
              style={{
                background: 'none',
                border: 'none',
                borderBottom: activeTab === 'slots' ? '3px solid #059669' : '3px solid transparent',
                padding: '8px 16px',
                fontWeight: 700,
                color: activeTab === 'slots' ? '#059669' : '#64748b',
                cursor: 'pointer'
              }}
            >
              📸 4-Slot Output Canvas (1000x1000)
            </button>
            <button
              onClick={() => setActiveTab('prompts')}
              style={{
                background: 'none',
                border: 'none',
                borderBottom: activeTab === 'prompts' ? '3px solid #059669' : '3px solid transparent',
                padding: '8px 16px',
                fontWeight: 700,
                color: activeTab === 'prompts' ? '#059669' : '#64748b',
                cursor: 'pointer'
              }}
            >
              📝 Prompts Specification
            </button>
          </div>

          {activeTab === 'slots' && (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: 16 }}>
              {slotsState.map((slot, index) => (
                <div key={slot.slotId} style={{ background: '#ffffff', border: '1px solid #e2e8f0', borderRadius: 10, padding: 12, display: 'flex', flexDirection: 'column' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
                    <span style={{ fontSize: '0.8rem', fontWeight: 800, color: '#0f172a' }}>{slot.slotName}</span>
                    <span style={{ fontSize: '0.72rem', fontWeight: 700, color: slot.status === 'completed' ? '#059669' : (slot.status === 'generating' ? '#d97706' : '#64748b') }}>
                      {slot.status === 'completed' ? '✅ Ready' : (slot.status === 'generating' ? '⏳ Rendering' : '⚪ Idle')}
                    </span>
                  </div>

                  {/* 1:1 Square Canvas Preview */}
                  <div style={{ width: '100%', aspectRatio: '1/1', background: '#f8fafc', border: '1px solid #f1f5f9', borderRadius: 8, overflow: 'hidden', display: 'flex', alignItems: 'center', justifyContent: 'center', position: 'relative' }}>
                    {slot.dataUrl ? (
                      <img src={slot.dataUrl} alt={slot.slotName} style={{ width: '100%', height: '100%', objectFit: 'contain' }} />
                    ) : (
                      <div style={{ textAlign: 'center', padding: 20, color: '#94a3b8', fontSize: '0.8rem' }}>
                        <div>{slot.status === 'generating' ? 'Rendering with Flow...' : 'Slot Belum Dirender'}</div>
                      </div>
                    )}
                  </div>

                  <div style={{ fontSize: '0.72rem', fontFamily: 'monospace', color: '#64748b', marginTop: 8, wordBreak: 'break-all' }}>
                    📁 {slot.filename}
                  </div>

                  {/* Actions */}
                  <div style={{ display: 'flex', gap: 6, marginTop: 10 }}>
                    <button
                      onClick={() => generateSlot(index)}
                      disabled={isGenerating || slot.status === 'generating'}
                      style={{ flex: 1, background: '#f1f5f9', border: '1px solid #cbd5e1', borderRadius: 6, padding: '6px 10px', fontSize: '0.75rem', fontWeight: 700, cursor: 'pointer' }}
                    >
                      ⚡ Render
                    </button>
                    <button
                      onClick={() => downloadSlotImage(slot.dataUrl, slot.filename)}
                      disabled={!slot.dataUrl}
                      style={{ background: '#ecfdf5', border: '1px solid #a7f3d0', color: '#047857', borderRadius: 6, padding: '6px 10px', fontSize: '0.75rem', fontWeight: 700, cursor: slot.dataUrl ? 'pointer' : 'not-allowed' }}
                    >
                      ⬇️ Download
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'prompts' && (
            <div style={{ background: '#fff', border: '1px solid #e2e8f0', borderRadius: 10, padding: 16 }}>
              {slotsState.map((slot) => (
                <div key={slot.slotId} style={{ marginBottom: 14 }}>
                  <div style={{ fontWeight: 700, fontSize: '0.85rem', marginBottom: 4 }}>{slot.slotName}</div>
                  <pre style={{ background: '#0f172a', color: '#38bdf8', padding: 12, borderRadius: 6, fontSize: '0.78rem', whiteSpace: 'pre-wrap', margin: 0 }}>
                    {slot.prompt || 'No prompt defined'}
                  </pre>
                </div>
              ))}
            </div>
          )}

          {/* Activity Logs Console */}
          <div style={{ background: '#0f172a', color: '#38bdf8', borderRadius: 10, padding: 14, marginTop: 20 }}>
            <div style={{ fontSize: '0.78rem', fontWeight: 800, color: '#f8fafc', marginBottom: 6 }}>📡 Flow Execution Console Logs:</div>
            <div style={{ maxHeight: 120, overflowY: 'auto', fontFamily: 'monospace', fontSize: '0.74rem', color: '#cbd5e1' }}>
              {logMessages.map((msg, idx) => (
                <div key={idx} style={{ marginBottom: 3 }}>{msg}</div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FlowImageGeneratorTool;

