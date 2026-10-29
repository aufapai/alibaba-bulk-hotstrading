# Alibaba.com Product Photo Guide (Footwear / AP Boots)

Internal SOP for preparing product photos for Alibaba.com listings, including a prompt library for AI-generated images (Google Flow) that keeps the product identical to the reference photo.

> **Verification note:** The specs below reflect common Alibaba.com / B2B marketplace practice. Exact limits (pixel size, number of images, file size) can change or vary by category. Always confirm in the Alibaba seller backend (Product Posting > image upload hints) before bulk production.

---

## 1. Image Set Overview (4 Images per Product)

| # | Slot | Purpose | Background |
|---|------|---------|------------|
| 1 | **Hero / Main image** | Search result thumbnail, first impression | Pure white (RGB 255,255,255) |
| 2 | **Side view A** | Show profile / opposite side of the shoe | Pure white |
| 3 | **Side view B** | Show rear, sole, or top view (pick the most informative angle for the model) | Pure white |
| 4 | **Usage shot** | Show the product in real context (worksite, rainy street, kitchen, etc.) | Realistic contextual scene |

Optional additions if the backend allows more slots: close-up detail (stitching, toe cap, sole pattern), packaging / carton shot, size chart, certification image.

---

## 2. Main Image (Hero) Requirements

**Background**
- Pure white, clean, no gradient, no texture, no visible floor line.
- Soft, natural contact shadow under the product is acceptable; hard or colored shadows are not.

**Composition**
- Square ratio **1:1**.
- Product fills roughly **80-90%** of the frame, centered, with even margins.
- Single product only (one shoe at a 3/4 angle, or one pair, but stay consistent across the catalog).
- Product fully in frame, nothing cropped.

**Technical**
- Minimum 750 x 750 px; target **1000 x 1000 px or larger** (zoom works better at higher resolution).
- Format: JPG (preferred) or PNG, sRGB color mode.
- Keep file size within the platform limit (typically a few MB; compress to quality 85-90).
- Sharp focus, even lighting, true-to-life color.

**Must not contain**
- Watermarks, other platform logos, QR codes, phone numbers, contact details.
- Promotional text overlays ("BEST PRICE", "HOT SALE"), badges, borders, collage.
- Props or accessories that are not included in the sale.
- Illustrations, obviously fake renders, or a product that differs from what is actually shipped.

---

## 3. Supporting Images (Slots 2 and 3)

- Same white background, same lighting, same scale as the hero so the set looks consistent.
- Recommended angles for footwear:
  - **Side profile** (full silhouette, height, shaft)
  - **Rear view** (heel, pull-tab, shaft shape)
  - **Sole / bottom view** (tread pattern, anti-slip, outsole material)
  - **Top / front view** (toe cap, opening, lining)
- Choose the two angles that answer the questions buyers ask most for that model (e.g. sole pattern for safety boots, shaft height for rain boots).
- Brand logo that is physically on the product is fine; do not add overlay logos.

---

## 4. Usage Shot (Slot 4)

- Realistic scene matching the target buyer segment:
  - Safety boots: factory floor, construction site, oil and gas site, warehouse.
  - Rain boots: wet street, farm, fishery, garden.
  - Kitchen / food-processing boots: clean wet kitchen, food plant floor.
  - Kids boots: rainy outdoor setting (only if appropriate for the lineup).
- Product must remain clearly visible and recognizable; the scene supports it, not the opposite.
- Avoid identifiable faces and real brand logos in the scene. Cropped legs / lower body framing is the safest approach.
- No text overlays; keep lighting natural; color of the product must match the real item.

---

## 5. AI Generation Rules (Google Flow)

Core principle: **the product must stay unchanged from the reference photos.** Any drift in shape, sole pattern, stitching, logo placement, color, or proportions is a listing-accuracy risk and can lead to buyer disputes or complaints.

**Always do**
1. Upload 2-3 real reference photos of the exact SKU (front 3/4, side, sole if available).
2. State explicitly: "Keep the product exactly identical to the reference images."
3. Generate at the highest available resolution, square 1:1.
4. Review every output against the reference before upload (see QA checklist).

**Never do**
- Let the model "improve" or redesign the product.
- Accept outputs with warped logos, extra seams, changed sole tread, or altered toe cap.
- Upload AI images without human comparison to the physical product.

---

## 6. Prompt Library

Replace the `[VARIABLES]` before each run.

**Variables**
- `[PRODUCT_TYPE]`: safety boots / rain boots / chef boots / kids rain boots / sandals
- `[COLOR]`: e.g. black, yellow, olive green
- `[KEY_FEATURES]`: e.g. steel toe cap, anti-slip outsole, waterproof PVC, oil-resistant sole
- `[BRAND]`: AP Boots (only if the logo is physically on the product)
- `[SCENE]`: usage environment for slot 4

### 6.1 Hero image (white background)

```
Using the attached reference photos, create a professional e-commerce product photo
of the exact same [COLOR] [PRODUCT_TYPE]. Keep the product exactly identical to the
reference: same shape, proportions, sole pattern, stitching, logo placement and color.
Single product, 3/4 front angle, standing upright, centered, filling about 85% of the
frame. Pure white seamless background (RGB 255,255,255), soft studio lighting, subtle
natural contact shadow only. Sharp focus, true-to-life color. Square 1:1, high
resolution. No text, no watermark, no props, no extra objects.
```

### 6.2 Side view A (profile)

```
Using the attached reference photos, create a product photo of the exact same
[COLOR] [PRODUCT_TYPE] from a straight side profile view. Keep the product exactly
identical to the reference. Pure white background (RGB 255,255,255), soft even studio
lighting, product centered and filling about 85% of the frame, subtle natural shadow.
Square 1:1, sharp focus, no text, no watermark, no props.
```

### 6.3 Side view B (choose one: rear / sole / top)

```
Using the attached reference photos, create a product photo of the exact same
[COLOR] [PRODUCT_TYPE] showing the [REAR VIEW | SOLE/BOTTOM VIEW | TOP-FRONT VIEW].
Keep the product exactly identical to the reference, especially [KEY_FEATURES].
Pure white background (RGB 255,255,255), soft even studio lighting, centered, about
85% of the frame. Square 1:1, sharp focus, no text, no watermark, no props.
```

### 6.4 Usage shot

```
Using the attached reference photos, create a realistic photo of the exact same
[COLOR] [PRODUCT_TYPE] being worn in [SCENE]. Frame from the knees down so the boots
are the clear focal point; no visible face. Keep the product exactly identical to the
reference: same shape, sole, stitching, logo placement and color. Natural lighting,
realistic environment, shallow depth of field on the background. Square 1:1, high
resolution. No text, no watermark, no overlay graphics.
```

### 6.5 Scene suggestions by product line

| Product | Suggested `[SCENE]` |
|---------|---------------------|
| Safety boots | "an industrial warehouse floor with concrete and yellow safety markings" |
| Oil and gas boots | "a refinery or oil rig work area, steel grating floor" |
| Rain boots | "a wet paved street after rain, puddles reflecting light" |
| Agriculture boots | "a muddy farm field with crops in the background" |
| Chef / kitchen boots | "a clean commercial kitchen with a wet tiled floor" |
| Kids boots | "a rainy sidewalk with fallen leaves" |

---

## 7. Post-Processing Checklist

- Crop / resize to **1:1**, export at **1000-2000 px** per side.
- Verify background is exactly RGB 255,255,255 on slots 1-3 (use eyedropper on corners).
- Confirm product fill is roughly 80-90% on slots 1-3.
- Export as JPG, quality 85-90, sRGB.
- File naming: `[sku]_[color]_[slot]_[view].jpg`, e.g. `APSAFETY-S3_black_01_hero.jpg`.
- Remove any metadata / watermark left by the generation tool.

---

## 8. QA Checklist (per image)

- [ ] Product matches the real SKU (shape, sole pattern, toe cap, stitching, logo position, color)
- [ ] No extra, missing, or distorted parts (laces, buckles, seams, pull-tabs)
- [ ] White background is clean (slots 1-3), no gray cast or floor line
- [ ] No text, logos of other brands, watermarks, or contact info
- [ ] Sharp, even lighting, color accurate
- [ ] Square 1:1, resolution at or above 1000 x 1000 px
- [ ] Usage shot: product clearly visible, scene realistic, no identifiable faces
- [ ] Set is visually consistent (same lighting, scale, and style across the 4 images)

---

## 9. Risks and Blind Spots

1. **Product drift.** AI models subtly alter soles, logos, and proportions. For safety footwear, a wrong toe cap or sole depiction is a compliance and trust problem, not just cosmetic. Mitigation: mandatory human comparison against the physical sample.
2. **Platform scrutiny of AI images.** Alibaba may flag or deprioritize misleading or low-quality visuals. Use AI to polish real products, not to invent features.
3. **Certification claims.** Never show certification marks (ISO, SNI, CE, etc.) in images unless the product is actually certified and documents are available.
4. **Consistency across the catalog.** Mixed styles hurt perceived professionalism. Lock one prompt template and one lighting description for the whole catalog.
5. **Real photos still win for critical SKUs.** For top-selling or high-value items, consider a short real photo session for the hero and use AI for secondary angles and usage shots.

---

## 10. Suggested Workflow for Internal Tooling

1. Input: SKU code, product type, color, key features, 2-3 reference photos.
2. Select prompt template (6.1 to 6.4) and fill variables.
3. Generate 4 images (hero, side A, side B, usage).
4. Auto-checks: resolution, aspect ratio, background pixel sampling on slots 1-3.
5. Human QA against the checklist in section 8.
6. Export with naming convention and upload to the Alibaba backend.
7. Log SKU, prompt version, and reviewer for traceability.
