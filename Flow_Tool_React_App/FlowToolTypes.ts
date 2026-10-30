// FlowToolTypes.ts
// Type definitions for Google Flow Tool React TypeScript App
// Target: https://flow.google.com/shared/tool/8afb2440-3207-4346-84ba-71796eb3028f

export interface FlowSlotPrompt {
  file: string;
  type: string;
  prompt: string;
  target_aspect_ratio: '1:1';
}

export interface FlowProductSlots {
  slot_1_hero: FlowSlotPrompt;
  slot_2_side: FlowSlotPrompt;
  slot_3_tread: FlowSlotPrompt;
  slot_4_usage: FlowSlotPrompt;
}

export interface FlowTargetConfig {
  account: string;
  project_id: string;
  project_url: string;
}

export interface PhotobankReadyConfig {
  category_folder: string;
  category_group: string;
  all_4_slots_ready: boolean;
}

export interface ProductFlowJson {
  product_identification: {
    sku: string;
    product_name_shopee: string;
    product_name_sanitized: string;
    brand: string;
    category?: string;
  };
  google_flow_and_photobank_slots?: {
    google_flow_target: FlowTargetConfig;
    slots_generated: FlowProductSlots;
    photobank_ready: PhotobankReadyConfig;
  };
  reference_images?: {
    hero_data_url?: string;
    side_data_url?: string;
  };
}

export interface GeneratedSlotResult {
  slotId: keyof FlowProductSlots;
  slotName: string;
  filename: string;
  dataUrl: string;
  prompt: string;
  status: 'pending' | 'generating' | 'completed' | 'error';
  error?: string;
}

// Global declaration for Google Flow SDK inside sandbox
declare global {
  interface Window {
    Flow?: {
      generate?: {
        image: (options: {
          prompt: string;
          referenceImage?: string;
          aspectRatio?: '1:1' | '16:9' | '9:16' | '4:3';
          safetySettings?: Record<string, any>;
        }) => Promise<{ imageUrl?: string; imageBase64?: string; mimeType?: string }>;
        text?: (options: { prompt: string }) => Promise<string>;
      };
    };
  }
}

