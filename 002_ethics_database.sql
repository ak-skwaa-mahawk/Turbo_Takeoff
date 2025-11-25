-- Turbo Takeoff Ethics Database Schema
-- Migration 002_ethics_database.sql

-- Companies table (suppliers, manufacturers)
CREATE TABLE companies (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  duns_number TEXT UNIQUE,
  ein TEXT,
  trade_categories TEXT[] DEFAULT '{}',
  website TEXT,
  phone TEXT,
  address JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Ethics data for each company
CREATE TABLE company_ethics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
  
  -- Ownership structure (10% of resonance score)
  indigenous_owned BOOLEAN DEFAULT FALSE,
  ancsa_corporation BOOLEAN DEFAULT FALSE,
  tribal_owned BOOLEAN DEFAULT FALSE,
  minority_owned BOOLEAN DEFAULT FALSE,
  woman_owned BOOLEAN DEFAULT FALSE,
  veteran_owned BOOLEAN DEFAULT FALSE,
  
  -- Certifications (10% of score)
  iaca_certified BOOLEAN DEFAULT FALSE,
  iaca_cert_date DATE,
  bbb_rating TEXT, -- A+, A, B, C, D, F, NR
  bbb_rating_date DATE,
  industry_certs JSONB DEFAULT '[]'::JSONB,
  
  -- Government compliance (40% of score)
  osha_violations_3yr INTEGER DEFAULT 0,
  osha_serious_violations_3yr INTEGER DEFAULT 0,
  osha_last_inspection DATE,
  epa_violations_3yr INTEGER DEFAULT 0,
  epa_fines_total_3yr DECIMAL(10,2) DEFAULT 0,
  labor_violations_3yr INTEGER DEFAULT 0,
  wage_theft_cases_3yr INTEGER DEFAULT 0,
  gsa_excluded BOOLEAN DEFAULT FALSE,
  gsa_exclusion_date DATE,
  
  -- Community standing (20% of score)
  user_reports_positive INTEGER DEFAULT 0,
  user_reports_negative INTEGER DEFAULT 0,
  tribal_endorsed BOOLEAN DEFAULT FALSE,
  tribal_endorsements TEXT[] DEFAULT '{}',
  community_violations TEXT[] DEFAULT '{}',
  
  -- Calculated resonance score (0-100)
  resonance_score INTEGER,
  score_calculated_at TIMESTAMPTZ,
  
  -- Metadata
  data_sources JSONB DEFAULT '{}'::JSONB,
  last_scraped_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- User relationship data with companies (20% of resonance)
CREATE TABLE user_company_relationships (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
  
  -- Usage tracking
  times_used INTEGER DEFAULT 0,
  first_used_at TIMESTAMPTZ DEFAULT NOW(),
  last_used_at TIMESTAMPTZ,
  
  -- Performance ratings (1-5 scale)
  avg_responsiveness DECIMAL(2,1),
  avg_delivery_time DECIMAL(2,1),
  avg_pricing_accuracy DECIMAL(2,1),
  avg_quality DECIMAL(2,1),
  personal_rating DECIMAL(2,1),
  
  -- Notes
  payment_terms_honored BOOLEAN DEFAULT TRUE,
  would_recommend BOOLEAN DEFAULT TRUE,
  notes TEXT,
  
  -- Priority ranking
  priority_rank INTEGER, -- 1 = first choice, 2 = second, etc.
  
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  
  UNIQUE(user_id, company_id)
);

-- User-submitted reports
CREATE TABLE user_reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  reporter_id UUID REFERENCES auth.users(id),
  company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
  
  report_type TEXT NOT NULL, -- 'positive', 'negative', 'neutral'
  category TEXT, -- 'quality', 'ethics', 'pricing', 'responsiveness', 'safety'
  
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  evidence_urls TEXT[] DEFAULT '{}',
  
  -- Verification
  verified BOOLEAN DEFAULT FALSE,
  verified_by UUID REFERENCES auth.users(id),
  verified_at TIMESTAMPTZ,
  confirmation_count INTEGER DEFAULT 0,
  
  -- Moderation
  flagged BOOLEAN DEFAULT FALSE,
  hidden BOOLEAN DEFAULT FALSE,
  moderator_notes TEXT,
  
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Pricing history tracking
CREATE TABLE pricing_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id),
  company_id UUID REFERENCES companies(id),
  
  material_name TEXT NOT NULL,
  manufacturer TEXT,
  product_code TEXT,
  
  unit_price DECIMAL(10,2) NOT NULL,
  unit_type TEXT NOT NULL, -- LF, SF, EA, CY, etc.
  quantity DECIMAL(10,2),
  
  quote_date DATE NOT NULL,
  valid_until DATE,
  
  region TEXT, -- Springfield MO, Anchorage AK, etc.
  project_type TEXT, -- residential, commercial, industrial
  
  notes TEXT,
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX idx_companies_name ON companies(name);
CREATE INDEX idx_companies_trade_categories ON companies USING GIN(trade_categories);
CREATE INDEX idx_company_ethics_company_id ON company_ethics(company_id);
CREATE INDEX idx_company_ethics_resonance_score ON company_ethics(resonance_score DESC);
CREATE INDEX idx_user_relationships_user_company ON user_company_relationships(user_id, company_id);
CREATE INDEX idx_user_relationships_priority ON user_company_relationships(user_id, priority_rank);
CREATE INDEX idx_user_reports_company ON user_reports(company_id, report_type);
CREATE INDEX idx_pricing_history_user_material ON pricing_history(user_id, material_name);
CREATE INDEX idx_pricing_history_date ON pricing_history(quote_date DESC);

-- Function to calculate resonance score
CREATE OR REPLACE FUNCTION calculate_resonance_score(
  company_ethics_id UUID,
  user_id UUID DEFAULT NULL
)
RETURNS INTEGER AS $$
DECLARE
  score INTEGER := 0;
  ethics_data RECORD;
  relationship_data RECORD;
BEGIN
  -- Get ethics data
  SELECT * INTO ethics_data
  FROM company_ethics
  WHERE id = company_ethics_id;
  
  -- Government Compliance (40 points max)
  -- Start at 40, deduct for violations
  score := 40;
  score := score - (ethics_data.osha_serious_violations_3yr * 5);
  score := score - (ethics_data.osha_violations_3yr * 2);
  score := score - (ethics_data.epa_violations_3yr * 3);
  score := score - (ethics_data.labor_violations_3yr * 5);
  score := score - (ethics_data.wage_theft_cases_3yr * 10);
  IF ethics_data.gsa_excluded THEN score := score - 20; END IF;
  score := GREATEST(score, 0); -- Floor at 0
  
  -- Community Standing (20 points max)
  score := score + LEAST(ethics_data.user_reports_positive, 10);
  score := score - (ethics_data.user_reports_negative * 2);
  IF ethics_data.tribal_endorsed THEN score := score + 10; END IF;
  
  -- Ownership Structure (10 points max)
  IF ethics_data.indigenous_owned OR ethics_data.tribal_owned THEN score := score + 5; END IF;
  IF ethics_data.ancsa_corporation THEN score := score + 3; END IF;
  IF ethics_data.minority_owned THEN score := score + 2; END IF;
  IF ethics_data.veteran_owned THEN score := score + 2; END IF;
  IF ethics_data.woman_owned THEN score := score + 2; END IF;
  
  -- Certifications (10 points max)
  IF ethics_data.iaca_certified THEN score := score + 5; END IF;
  IF ethics_data.bbb_rating IN ('A+', 'A') THEN score := score + 5;
  ELSIF ethics_data.bbb_rating = 'B' THEN score := score + 3;
  END IF;
  
  -- User Relationship (20 points max) - only if user_id provided
  IF user_id IS NOT NULL THEN
    SELECT * INTO relationship_data
    FROM user_company_relationships
    WHERE user_company_relationships.user_id = calculate_resonance_score.user_id
      AND user_company_relationships.company_id = ethics_data.company_id;
    
    IF FOUND THEN
      -- Frequent use bonus
      IF relationship_data.times_used > 10 THEN score := score + 5;
      ELSIF relationship_data.times_used > 5 THEN score := score + 3;
      END IF;
      
      -- Performance ratings
      IF relationship_data.personal_rating IS NOT NULL THEN
        score := score + (relationship_data.personal_rating * 2)::INTEGER;
      END IF;
      
      -- Reliability
      IF relationship_data.payment_terms_honored THEN score := score + 3; END IF;
      IF relationship_data.would_recommend THEN score := score + 2; END IF;
    END IF;
  END IF;
  
  -- Cap at 100
  score := LEAST(score, 100);
  
  -- Update the score in the database
  UPDATE company_ethics
  SET resonance_score = score,
      score_calculated_at = NOW()
  WHERE id = company_ethics_id;
  
  RETURN score;
END;
$$ LANGUAGE plpgsql;

-- Trigger to recalculate score on ethics data update
CREATE OR REPLACE FUNCTION trigger_recalculate_resonance()
RETURNS TRIGGER AS $$
BEGIN
  PERFORM calculate_resonance_score(NEW.id);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER recalculate_resonance_on_update
AFTER INSERT OR UPDATE ON company_ethics
FOR EACH ROW
EXECUTE FUNCTION trigger_recalculate_resonance();

-- View for easy company lookup with resonance scores
CREATE OR REPLACE VIEW companies_with_resonance AS
SELECT 
  c.*,
  ce.resonance_score,
  ce.indigenous_owned,
  ce.veteran_owned,
  ce.iaca_certified,
  ce.bbb_rating,
  ce.tribal_endorsed,
  ce.score_calculated_at
FROM companies c
LEFT JOIN company_ethics ce ON c.id = ce.company_id
ORDER BY ce.resonance_score DESC NULLS LAST;

-- RLS (Row Level Security) policies
ALTER TABLE companies ENABLE ROW LEVEL SECURITY;
ALTER TABLE company_ethics ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_company_relationships ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE pricing_history ENABLE ROW LEVEL SECURITY;

-- Public can read companies and ethics data
CREATE POLICY "Companies are viewable by everyone"
  ON companies FOR SELECT
  USING (true);

CREATE POLICY "Company ethics viewable by everyone"
  ON company_ethics FOR SELECT
  USING (true);

-- Users can only modify their own relationship data
CREATE POLICY "Users can view their own relationships"
  ON user_company_relationships FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own relationships"
  ON user_company_relationships FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own relationships"
  ON user_company_relationships FOR UPDATE
  USING (auth.uid() = user_id);

-- Users can submit reports
CREATE POLICY "Users can submit reports"
  ON user_reports FOR INSERT
  WITH CHECK (auth.uid() = reporter_id);

CREATE POLICY "Users can view verified reports"
  ON user_reports FOR SELECT
  USING (verified = true AND hidden = false);

-- Users can only access their own pricing history
CREATE POLICY "Users can view their pricing history"
  ON pricing_history FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their pricing history"
  ON pricing_history FOR INSERT
  WITH CHECK (auth.uid() = user_id);