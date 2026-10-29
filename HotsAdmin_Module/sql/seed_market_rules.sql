-- ==============================================================================
-- HOTS TRADING - MARKET RULES SEED DATA (5 Continents Q1 - Q4)
-- File: sql/seed_market_rules.sql
-- ==============================================================================

INSERT INTO `alibaba_market_rules` (`continent`, `top_countries`, `quarter`, `seasonal_demand_trigger`, `recommended_angle`, `mandatory_certifications`, `recommended_keywords`, `is_active`) VALUES
-- Q4 (Oktober - Desember)
('Europe', '["Germany", "United Kingdom", "Netherlands", "France", "Poland"]', 'Q4', 'Late Autumn rain, early frost & wet mud operations. Year-end PPE procurement.', 'Heavy Industrial & Construction', 'CE EN ISO 20345 (S4/S5), Oeko-Tex Standard 100', '["safety boots S5", "waterproof work boots", "steel toe safety boots", "EN 20345 boots"]', 1),
('North America', '["United States", "Canada", "Mexico"]', 'Q4', 'Pre-winter storm preparation, outdoor construction foundations & logistics.', 'Civil Construction & Infrastructure', 'ASTM F2413-18, OSHA Standard Compliance', '["industrial rubber boots", "steel toe work boots", "mud boots waterproof", "heavy duty rain boots"]', 1),
('Southeast Asia', '["Malaysia", "Thailand", "Philippines", "Vietnam", "Singapore"]', 'Q4', 'Peak monsoon tropical rainy season & palm oil plantation mud terrain.', 'Agricultural & Commercial Mud Utility', 'SNI (Standar Nasional Indonesia), TKDN > 50%', '["waterproof rubber boots", "anti slip boots", "plantation boots", "heavy duty pvc boots"]', 1),
('Middle East', '["United Arab Emirates", "Saudi Arabia", "Qatar", "Kuwait"]', 'Q4', 'Mega infrastructure foundations, oil & gas maintenance yards, luxury hotel kitchen prep.', 'Petrochemical & Food Industry Utility', 'ISO 9001/14001, Heat Resistant Outsole Test', '["safety boots Dubai", "oil resistant boots", "slip resistant kitchen clogs", "industrial gumboots"]', 1),
('Oceania', '["Australia", "New Zealand"]', 'Q4', 'Spring transition to summer. Heavy agricultural harvesting & mining expeditions.', 'Mining Sector Heavy Duty', 'AS/NZS 2210.3, Slip Resistance Class SRC', '["mining safety boots", "agricultural work boots", "gumboots steel cap", "waterproof farm boots"]', 1),

-- Q1 (Januari - Maret)
('Europe', '["Germany", "France", "Italy", "Spain"]', 'Q1', 'Spring thaw thaw flooding, municipal drainage & road works reactivation.', 'Municipal Utility & Civil Works', 'CE EN ISO 20345 S4/S5', '["drainage boots waterproof", "civil work boots", "construction safety boots", "anti slip gumboots"]', 1),
('Southeast Asia', '["Indonesia", "Malaysia", "Thailand"]', 'Q1', 'Palm oil harvesting cycle 1 & fishery harbor logistics.', 'Fishery & Palm Oil Industrial', 'SNI, ISO 9001', '["fishery waterproof boots", "oil palm harvesting boots", "pvc safety boots yellow", "mud boots"]', 1)

ON DUPLICATE KEY UPDATE 
  `seasonal_demand_trigger` = VALUES(`seasonal_demand_trigger`),
  `recommended_angle` = VALUES(`recommended_angle`),
  `is_active` = 1;
