# GOOGLE FLOW 10-PRODUCT AGENT MASTER PROMPT

```text
[GOOGLE FLOW AGENT MASTER PROMPT - ALWAYS-APPROVE BATCH MODE]
Target Project: https://flow.google.com/project/5a88c3fd-477c-4eed-a126-f812ccfb079c
Target Account: aufahots@gmail.com
Execution Policy: ALWAYS_APPROVE (Autonomous sequential generation without manual confirm prompts)
Total Products: 10 Products (4 Slots per Product = 40 Output Images)

ROLE & OBJECTIVE:
You are the Autonomous E-Commerce Visual Production Agent for PT Indo Sukses Semesta / PT Waru Gunung (HOTS Trading).
Your task is to generate 4 photorealistic square (1:1, 1000x1000) e-commerce product photos for each product in the coupled JSON list below.

SLOT SPECIFICATIONS:
1. Slot 1 (hero_[folder].webp): Front 3/4 perspective studio hero shot on seamless pure white (#FFFFFF / RGB 255,255,255).
2. Slot 2 (side_[folder].webp): Orthogonal 90° lateral side profile showcasing shaft height, vamp curvature, and sole thickness on pure white (#FFFFFF).
3. Slot 3 (tread_[folder].webp): Macro bottom outsole tread detailing traction cleats, lug patterns, and mud channels on pure white (#FFFFFF).
4. Slot 4 (usage_[folder].webp): Realistic contextual in-use photo on wet outdoor agricultural plantation / industrial muddy ground (knees down, no faces).

DOWNLOAD CONVENTION:
Save/download each file strictly according to the 'target_filenames' specified in the coupled JSON.

COUPLED 10-PRODUCT DATA JSON:
[
  {
    "sku": "SHP-001",
    "product_name": "AP Boots XTR Hitam - Sepatu Boot PVC",
    "folder_name": "AP_Boots_XTR_Hitam_Sepatu_Boot_PVC",
    "brand": "AP Boots",
    "price_idr": "73.900",
    "category": "Agricultural & General Industrial Rubber Boots",
    "target_filenames": {
      "slot_1_hero": "hero_AP_Boots_XTR_Hitam_Sepatu_Boot_PVC.webp",
      "slot_2_side": "side_AP_Boots_XTR_Hitam_Sepatu_Boot_PVC.webp",
      "slot_3_tread": "tread_AP_Boots_XTR_Hitam_Sepatu_Boot_PVC.webp",
      "slot_4_usage": "usage_AP_Boots_XTR_Hitam_Sepatu_Boot_PVC.webp"
    },
    "slot_prompts": {
      "slot_1_hero": "Commercial studio product photograph of AP Boots XTR Hitam - Sepatu Boot PVC. Front 3/4 angle, standing upright, centered, occupying 85% frame. Seamless pure white background (#FFFFFF / RGB 255,255,255), soft even studio lighting, crisp waterproof PVC rubber boot texture, clean sole treads, photorealistic 8k, square 1:1, no watermark, no text.",
      "slot_2_side": "Clean e-commerce commercial product photograph of AP Boots XTR Hitam - Sepatu Boot PVC from a straight orthogonal 90-degree lateral side profile view. Highlighting boot shaft height, waterproof seamless contour, and sole thickness. Seamless pure white background (#FFFFFF / RGB 255,255,255), square 1:1 ratio, no text.",
      "slot_3_tread": "High-definition commercial product photo of AP Boots XTR Hitam - Sepatu Boot PVC showcasing the bottom outsole tread pattern and anti-slip traction lugs. Pure white background (#FFFFFF), square 1:1 ratio, sharp macro focus, no text.",
      "slot_4_usage": "Realistic contextual photograph of AP Boots XTR Hitam - Sepatu Boot PVC being actively worn on wet agricultural plantation terrain and muddy ground in outdoor daylight. Lower-body framing from knees down, no visible human faces, square 1:1 ratio, photorealistic."
    },
    "status": {
      "hero_exists": true,
      "side_exists": true,
      "tread_exists": true,
      "usage_exists": true,
      "json_exists": true
    }
  },
  {
    "sku": "SHP-002",
    "product_name": "AP Boots AP 1 Hitam - Sepatu Boots PVC",
    "folder_name": "AP_Boots_AP_1_Hitam_Sepatu_Boots_PVC",
    "brand": "AP Boots",
    "price_idr": "84.900",
    "category": "Agricultural & General Industrial Rubber Boots",
    "target_filenames": {
      "slot_1_hero": "hero_AP_Boots_AP_1_Hitam_Sepatu_Boots_PVC.webp",
      "slot_2_side": "side_AP_Boots_AP_1_Hitam_Sepatu_Boots_PVC.webp",
      "slot_3_tread": "tread_AP_Boots_AP_1_Hitam_Sepatu_Boots_PVC.webp",
      "slot_4_usage": "usage_AP_Boots_AP_1_Hitam_Sepatu_Boots_PVC.webp"
    },
    "slot_prompts": {
      "slot_1_hero": "Commercial studio product photograph of AP Boots AP 1 Hitam - Sepatu Boots PVC. Front 3/4 angle, standing upright, centered, occupying 85% frame. Seamless pure white background (#FFFFFF / RGB 255,255,255), soft even studio lighting, crisp waterproof PVC rubber boot texture, clean sole treads, photorealistic 8k, square 1:1, no watermark, no text.",
      "slot_2_side": "Clean e-commerce commercial product photograph of AP Boots AP 1 Hitam - Sepatu Boots PVC from a straight orthogonal 90-degree lateral side profile view. Highlighting boot shaft height, waterproof seamless contour, and sole thickness. Seamless pure white background (#FFFFFF / RGB 255,255,255), square 1:1 ratio, no text.",
      "slot_3_tread": "High-definition commercial product photo of AP Boots AP 1 Hitam - Sepatu Boots PVC showcasing the bottom outsole tread pattern and anti-slip traction lugs. Pure white background (#FFFFFF), square 1:1 ratio, sharp macro focus, no text.",
      "slot_4_usage": "Realistic contextual photograph of AP Boots AP 1 Hitam - Sepatu Boots PVC being actively worn on wet agricultural plantation terrain and muddy ground in outdoor daylight. Lower-body framing from knees down, no visible human faces, square 1:1 ratio, photorealistic."
    },
    "status": {
      "hero_exists": true,
      "side_exists": true,
      "tread_exists": true,
      "usage_exists": true,
      "json_exists": true
    }
  },
  {
    "sku": "SHP-003",
    "product_name": "AP Boots AP Chef Hitam - Sepatu Slip On Dapur",
    "folder_name": "AP_Boots_AP_Chef_Hitam_Sepatu_Slip_On_Dapur",
    "brand": "AP Boots",
    "price_idr": "229.000",
    "category": "Workplace Hygiene & Hospitality Footwear",
    "target_filenames": {
      "slot_1_hero": "hero_AP_Boots_AP_Chef_Hitam_Sepatu_Slip_On_Dapur.webp",
      "slot_2_side": "side_AP_Boots_AP_Chef_Hitam_Sepatu_Slip_On_Dapur.webp",
      "slot_3_tread": "tread_AP_Boots_AP_Chef_Hitam_Sepatu_Slip_On_Dapur.webp",
      "slot_4_usage": "usage_AP_Boots_AP_Chef_Hitam_Sepatu_Slip_On_Dapur.webp"
    },
    "slot_prompts": {
      "slot_1_hero": "Commercial studio product photograph of AP Boots AP Chef Hitam - Sepatu Slip On Dapur. Front 3/4 angle, standing upright, centered, occupying 85% frame. Seamless pure white background (#FFFFFF / RGB 255,255,255), soft even studio lighting, crisp waterproof PVC rubber boot texture, clean sole treads, photorealistic 8k, square 1:1, no watermark, no text.",
      "slot_2_side": "Clean e-commerce commercial product photograph of AP Boots AP Chef Hitam - Sepatu Slip On Dapur from a straight orthogonal 90-degree lateral side profile view. Highlighting boot shaft height, waterproof seamless contour, and sole thickness. Seamless pure white background (#FFFFFF / RGB 255,255,255), square 1:1 ratio, no text.",
      "slot_3_tread": "High-definition commercial product photo of AP Boots AP Chef Hitam - Sepatu Slip On Dapur showcasing the bottom outsole tread pattern and anti-slip traction lugs. Pure white background (#FFFFFF), square 1:1 ratio, sharp macro focus, no text.",
      "slot_4_usage": "Realistic contextual photograph of AP Boots AP Chef Hitam - Sepatu Slip On Dapur being actively worn on wet agricultural plantation terrain and muddy ground in outdoor daylight. Lower-body framing from knees down, no visible human faces, square 1:1 ratio, photorealistic."
    },
    "status": {
      "hero_exists": true,
      "side_exists": true,
      "tread_exists": true,
      "usage_exists": true,
      "json_exists": true
    }
  },
  {
    "sku": "SHP-004",
    "product_name": "AP Boots TERRA GP Hijau - Sepatu Boot PVC",
    "folder_name": "AP_Boots_TERRA_GP_Hijau_Sepatu_Boot_PVC",
    "brand": "AP Boots",
    "price_idr": "94.400",
    "category": "Agricultural & General Industrial Rubber Boots",
    "target_filenames": {
      "slot_1_hero": "hero_AP_Boots_TERRA_GP_Hijau_Sepatu_Boot_PVC.webp",
      "slot_2_side": "side_AP_Boots_TERRA_GP_Hijau_Sepatu_Boot_PVC.webp",
      "slot_3_tread": "tread_AP_Boots_TERRA_GP_Hijau_Sepatu_Boot_PVC.webp",
      "slot_4_usage": "usage_AP_Boots_TERRA_GP_Hijau_Sepatu_Boot_PVC.webp"
    },
    "slot_prompts": {
      "slot_1_hero": "Commercial studio product photograph of AP Boots TERRA GP Hijau - Sepatu Boot PVC. Front 3/4 angle, standing upright, centered, occupying 85% frame. Seamless pure white background (#FFFFFF / RGB 255,255,255), soft even studio lighting, crisp waterproof PVC rubber boot texture, clean sole treads, photorealistic 8k, square 1:1, no watermark, no text.",
      "slot_2_side": "Clean e-commerce commercial product photograph of AP Boots TERRA GP Hijau - Sepatu Boot PVC from a straight orthogonal 90-degree lateral side profile view. Highlighting boot shaft height, waterproof seamless contour, and sole thickness. Seamless pure white background (#FFFFFF / RGB 255,255,255), square 1:1 ratio, no text.",
      "slot_3_tread": "High-definition commercial product photo of AP Boots TERRA GP Hijau - Sepatu Boot PVC showcasing the bottom outsole tread pattern and anti-slip traction lugs. Pure white background (#FFFFFF), square 1:1 ratio, sharp macro focus, no text.",
      "slot_4_usage": "Realistic contextual photograph of AP Boots TERRA GP Hijau - Sepatu Boot PVC being actively worn on wet agricultural plantation terrain and muddy ground in outdoor daylight. Lower-body framing from knees down, no visible human faces, square 1:1 ratio, photorealistic."
    },
    "status": {
      "hero_exists": true,
      "side_exists": true,
      "tread_exists": true,
      "usage_exists": true,
      "json_exists": true
    }
  },
  {
    "sku": "SHP-005",
    "product_name": "AP Boots TERRA GP Hitam - Sepatu Boot PVC",
    "folder_name": "AP_Boots_TERRA_GP_Hitam_Sepatu_Boot_PVC",
    "brand": "AP Boots",
    "price_idr": "83.900",
    "category": "Agricultural & General Industrial Rubber Boots",
    "target_filenames": {
      "slot_1_hero": "hero_AP_Boots_TERRA_GP_Hitam_Sepatu_Boot_PVC.webp",
      "slot_2_side": "side_AP_Boots_TERRA_GP_Hitam_Sepatu_Boot_PVC.webp",
      "slot_3_tread": "tread_AP_Boots_TERRA_GP_Hitam_Sepatu_Boot_PVC.webp",
      "slot_4_usage": "usage_AP_Boots_TERRA_GP_Hitam_Sepatu_Boot_PVC.webp"
    },
    "slot_prompts": {
      "slot_1_hero": "Commercial studio product photograph of AP Boots TERRA GP Hitam - Sepatu Boot PVC. Front 3/4 angle, standing upright, centered, occupying 85% frame. Seamless pure white background (#FFFFFF / RGB 255,255,255), soft even studio lighting, crisp waterproof PVC rubber boot texture, clean sole treads, photorealistic 8k, square 1:1, no watermark, no text.",
      "slot_2_side": "Clean e-commerce commercial product photograph of AP Boots TERRA GP Hitam - Sepatu Boot PVC from a straight orthogonal 90-degree lateral side profile view. Highlighting boot shaft height, waterproof seamless contour, and sole thickness. Seamless pure white background (#FFFFFF / RGB 255,255,255), square 1:1 ratio, no text.",
      "slot_3_tread": "High-definition commercial product photo of AP Boots TERRA GP Hitam - Sepatu Boot PVC showcasing the bottom outsole tread pattern and anti-slip traction lugs. Pure white background (#FFFFFF), square 1:1 ratio, sharp macro focus, no text.",
      "slot_4_usage": "Realistic contextual photograph of AP Boots TERRA GP Hitam - Sepatu Boot PVC being actively worn on wet agricultural plantation terrain and muddy ground in outdoor daylight. Lower-body framing from knees down, no visible human faces, square 1:1 ratio, photorealistic."
    },
    "status": {
      "hero_exists": true,
      "side_exists": true,
      "tread_exists": true,
      "usage_exists": true,
      "json_exists": true
    }
  },
  {
    "sku": "SHP-006",
    "product_name": "AP Boots 2017 Green - Sepatu Boot PVC",
    "folder_name": "AP_Boots_2017_Green_Sepatu_Boot_PVC",
    "brand": "AP Boots",
    "price_idr": "131.400",
    "category": "Agricultural & General Industrial Rubber Boots",
    "target_filenames": {
      "slot_1_hero": "hero_AP_Boots_2017_Green_Sepatu_Boot_PVC.webp",
      "slot_2_side": "side_AP_Boots_2017_Green_Sepatu_Boot_PVC.webp",
      "slot_3_tread": "tread_AP_Boots_2017_Green_Sepatu_Boot_PVC.webp",
      "slot_4_usage": "usage_AP_Boots_2017_Green_Sepatu_Boot_PVC.webp"
    },
    "slot_prompts": {
      "slot_1_hero": "Commercial studio product photograph of AP Boots 2017 Green - Sepatu Boot PVC. Front 3/4 angle, standing upright, centered, occupying 85% frame. Seamless pure white background (#FFFFFF / RGB 255,255,255), soft even studio lighting, crisp waterproof PVC rubber boot texture, clean sole treads, photorealistic 8k, square 1:1, no watermark, no text.",
      "slot_2_side": "Clean e-commerce commercial product photograph of AP Boots 2017 Green - Sepatu Boot PVC from a straight orthogonal 90-degree lateral side profile view. Highlighting boot shaft height, waterproof seamless contour, and sole thickness. Seamless pure white background (#FFFFFF / RGB 255,255,255), square 1:1 ratio, no text.",
      "slot_3_tread": "High-definition commercial product photo of AP Boots 2017 Green - Sepatu Boot PVC showcasing the bottom outsole tread pattern and anti-slip traction lugs. Pure white background (#FFFFFF), square 1:1 ratio, sharp macro focus, no text.",
      "slot_4_usage": "Realistic contextual photograph of AP Boots 2017 Green - Sepatu Boot PVC being actively worn on wet agricultural plantation terrain and muddy ground in outdoor daylight. Lower-body framing from knees down, no visible human faces, square 1:1 ratio, photorealistic."
    },
    "status": {
      "hero_exists": true,
      "side_exists": true,
      "tread_exists": true,
      "usage_exists": true,
      "json_exists": true
    }
  },
  {
    "sku": "SHP-007",
    "product_name": "AP Boots TERRA ECO 3 Hitam - Sepatu Boot PVC",
    "folder_name": "AP_Boots_TERRA_ECO_3_Hitam_Sepatu_Boot_PVC",
    "brand": "AP Boots",
    "price_idr": "118.900",
    "category": "Agricultural & General Industrial Rubber Boots",
    "target_filenames": {
      "slot_1_hero": "hero_AP_Boots_TERRA_ECO_3_Hitam_Sepatu_Boot_PVC.webp",
      "slot_2_side": "side_AP_Boots_TERRA_ECO_3_Hitam_Sepatu_Boot_PVC.webp",
      "slot_3_tread": "tread_AP_Boots_TERRA_ECO_3_Hitam_Sepatu_Boot_PVC.webp",
      "slot_4_usage": "usage_AP_Boots_TERRA_ECO_3_Hitam_Sepatu_Boot_PVC.webp"
    },
    "slot_prompts": {
      "slot_1_hero": "Commercial studio product photograph of AP Boots TERRA ECO 3 Hitam - Sepatu Boot PVC. Front 3/4 angle, standing upright, centered, occupying 85% frame. Seamless pure white background (#FFFFFF / RGB 255,255,255), soft even studio lighting, crisp waterproof PVC rubber boot texture, clean sole treads, photorealistic 8k, square 1:1, no watermark, no text.",
      "slot_2_side": "Clean e-commerce commercial product photograph of AP Boots TERRA ECO 3 Hitam - Sepatu Boot PVC from a straight orthogonal 90-degree lateral side profile view. Highlighting boot shaft height, waterproof seamless contour, and sole thickness. Seamless pure white background (#FFFFFF / RGB 255,255,255), square 1:1 ratio, no text.",
      "slot_3_tread": "High-definition commercial product photo of AP Boots TERRA ECO 3 Hitam - Sepatu Boot PVC showcasing the bottom outsole tread pattern and anti-slip traction lugs. Pure white background (#FFFFFF), square 1:1 ratio, sharp macro focus, no text.",
      "slot_4_usage": "Realistic contextual photograph of AP Boots TERRA ECO 3 Hitam - Sepatu Boot PVC being actively worn on wet agricultural plantation terrain and muddy ground in outdoor daylight. Lower-body framing from knees down, no visible human faces, square 1:1 ratio, photorealistic."
    },
    "status": {
      "hero_exists": true,
      "side_exists": true,
      "tread_exists": true,
      "usage_exists": true,
      "json_exists": true
    }
  },
  {
    "sku": "SHP-008",
    "product_name": "Ap Boots 9905 HITAM - Sepatu Boots PVC",
    "folder_name": "Ap_Boots_9905_HITAM_Sepatu_Boots_PVC",
    "brand": "AP Boots",
    "price_idr": "129.400",
    "category": "Agricultural & General Industrial Rubber Boots",
    "target_filenames": {
      "slot_1_hero": "hero_Ap_Boots_9905_HITAM_Sepatu_Boots_PVC.webp",
      "slot_2_side": "side_Ap_Boots_9905_HITAM_Sepatu_Boots_PVC.webp",
      "slot_3_tread": "tread_Ap_Boots_9905_HITAM_Sepatu_Boots_PVC.webp",
      "slot_4_usage": "usage_Ap_Boots_9905_HITAM_Sepatu_Boots_PVC.webp"
    },
    "slot_prompts": {
      "slot_1_hero": "Commercial studio product photograph of Ap Boots 9905 HITAM - Sepatu Boots PVC. Front 3/4 angle, standing upright, centered, occupying 85% frame. Seamless pure white background (#FFFFFF / RGB 255,255,255), soft even studio lighting, crisp waterproof PVC rubber boot texture, clean sole treads, photorealistic 8k, square 1:1, no watermark, no text.",
      "slot_2_side": "Clean e-commerce commercial product photograph of Ap Boots 9905 HITAM - Sepatu Boots PVC from a straight orthogonal 90-degree lateral side profile view. Highlighting boot shaft height, waterproof seamless contour, and sole thickness. Seamless pure white background (#FFFFFF / RGB 255,255,255), square 1:1 ratio, no text.",
      "slot_3_tread": "High-definition commercial product photo of Ap Boots 9905 HITAM - Sepatu Boots PVC showcasing the bottom outsole tread pattern and anti-slip traction lugs. Pure white background (#FFFFFF), square 1:1 ratio, sharp macro focus, no text.",
      "slot_4_usage": "Realistic contextual photograph of Ap Boots 9905 HITAM - Sepatu Boots PVC being actively worn on wet agricultural plantation terrain and muddy ground in outdoor daylight. Lower-body framing from knees down, no visible human faces, square 1:1 ratio, photorealistic."
    },
    "status": {
      "hero_exists": true,
      "side_exists": true,
      "tread_exists": true,
      "usage_exists": true,
      "json_exists": true
    }
  },
  {
    "sku": "SHP-009",
    "product_name": "AP Boots MOTO 2 - Sepatu Boot PVC",
    "folder_name": "AP_Boots_MOTO_2_Sepatu_Boot_PVC",
    "brand": "AP Boots",
    "price_idr": "152.400",
    "category": "Water-Resistant Daily Footwear & Splash Protection",
    "target_filenames": {
      "slot_1_hero": "hero_AP_Boots_MOTO_2_Sepatu_Boot_PVC.webp",
      "slot_2_side": "side_AP_Boots_MOTO_2_Sepatu_Boot_PVC.webp",
      "slot_3_tread": "tread_AP_Boots_MOTO_2_Sepatu_Boot_PVC.webp",
      "slot_4_usage": "usage_AP_Boots_MOTO_2_Sepatu_Boot_PVC.webp"
    },
    "slot_prompts": {
      "slot_1_hero": "Commercial studio product photograph of AP Boots MOTO 2 - Sepatu Boot PVC. Front 3/4 angle, standing upright, centered, occupying 85% frame. Seamless pure white background (#FFFFFF / RGB 255,255,255), soft even studio lighting, crisp waterproof PVC rubber boot texture, clean sole treads, photorealistic 8k, square 1:1, no watermark, no text.",
      "slot_2_side": "Clean e-commerce commercial product photograph of AP Boots MOTO 2 - Sepatu Boot PVC from a straight orthogonal 90-degree lateral side profile view. Highlighting boot shaft height, waterproof seamless contour, and sole thickness. Seamless pure white background (#FFFFFF / RGB 255,255,255), square 1:1 ratio, no text.",
      "slot_3_tread": "High-definition commercial product photo of AP Boots MOTO 2 - Sepatu Boot PVC showcasing the bottom outsole tread pattern and anti-slip traction lugs. Pure white background (#FFFFFF), square 1:1 ratio, sharp macro focus, no text.",
      "slot_4_usage": "Realistic contextual photograph of AP Boots MOTO 2 - Sepatu Boot PVC being actively worn on wet agricultural plantation terrain and muddy ground in outdoor daylight. Lower-body framing from knees down, no visible human faces, square 1:1 ratio, photorealistic."
    },
    "status": {
      "hero_exists": true,
      "side_exists": true,
      "tread_exists": true,
      "usage_exists": true,
      "json_exists": true
    }
  },
  {
    "sku": "SHP-010",
    "product_name": "AP Boots 2018 Ultraflex Abu - Sepatu Boot PVC",
    "folder_name": "AP_Boots_2018_Ultraflex_Abu_Sepatu_Boot_PVC",
    "brand": "AP Boots",
    "price_idr": "200.900",
    "category": "Agricultural & General Industrial Rubber Boots",
    "target_filenames": {
      "slot_1_hero": "hero_AP_Boots_2018_Ultraflex_Abu_Sepatu_Boot_PVC.webp",
      "slot_2_side": "side_AP_Boots_2018_Ultraflex_Abu_Sepatu_Boot_PVC.webp",
      "slot_3_tread": "tread_AP_Boots_2018_Ultraflex_Abu_Sepatu_Boot_PVC.webp",
      "slot_4_usage": "usage_AP_Boots_2018_Ultraflex_Abu_Sepatu_Boot_PVC.webp"
    },
    "slot_prompts": {
      "slot_1_hero": "Commercial studio product photograph of AP Boots 2018 Ultraflex Abu - Sepatu Boot PVC. Front 3/4 angle, standing upright, centered, occupying 85% frame. Seamless pure white background (#FFFFFF / RGB 255,255,255), soft even studio lighting, crisp waterproof PVC rubber boot texture, clean sole treads, photorealistic 8k, square 1:1, no watermark, no text.",
      "slot_2_side": "Clean e-commerce commercial product photograph of AP Boots 2018 Ultraflex Abu - Sepatu Boot PVC from a straight orthogonal 90-degree lateral side profile view. Highlighting boot shaft height, waterproof seamless contour, and sole thickness. Seamless pure white background (#FFFFFF / RGB 255,255,255), square 1:1 ratio, no text.",
      "slot_3_tread": "High-definition commercial product photo of AP Boots 2018 Ultraflex Abu - Sepatu Boot PVC showcasing the bottom outsole tread pattern and anti-slip traction lugs. Pure white background (#FFFFFF), square 1:1 ratio, sharp macro focus, no text.",
      "slot_4_usage": "Realistic contextual photograph of AP Boots 2018 Ultraflex Abu - Sepatu Boot PVC being actively worn on wet agricultural plantation terrain and muddy ground in outdoor daylight. Lower-body framing from knees down, no visible human faces, square 1:1 ratio, photorealistic."
    },
    "status": {
      "hero_exists": true,
      "side_exists": true,
      "tread_exists": true,
      "usage_exists": true,
      "json_exists": true
    }
  }
]

```
