"""
Privacy Policy Analysis Tool
Analyzes privacy policies for P6 (Visibility and Transparency) scoring
Part of Privacy by Design Implementation Score (PBDIS) framework
"""

import requests
from bs4 import BeautifulSoup
import textstat
import pandas as pd
import re
from datetime import datetime
import json

class PrivacyPolicyAnalyzer:
    """Analyzes privacy policies and calculates P6 transparency scores"""
    
    def __init__(self):
        self.policies = {
            'Meta': 'https://www.facebook.com/privacy/policy/',
            'Google': 'https://policies.google.com/privacy',
            'Microsoft': 'https://privacy.microsoft.com/en-us/privacystatement',
            'Proton': 'https://proton.me/legal/privacy'
        }
        
        self.results = []
    
    def extract_text_from_url(self, url):
        """Extract clean text from privacy policy URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Get text
            text = soup.get_text(separator=' ', strip=True)
            
            # Clean up whitespace
            text = re.sub(r'\s+', ' ', text)
            
            return text
        
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def analyze_readability(self, text):
        """Calculate readability metrics"""
        if not text or len(text) < 100:
            return None
        
        metrics = {
            'flesch_reading_ease': textstat.flesch_reading_ease(text),
            'flesch_kincaid_grade': textstat.flesch_kincaid_grade(text),
            'gunning_fog': textstat.gunning_fog(text),
            'smog_index': textstat.smog_index(text),
            'coleman_liau_index': textstat.coleman_liau_index(text),
            'automated_readability_index': textstat.automated_readability_index(text),
            'dale_chall_readability_score': textstat.dale_chall_readability_score(text),
            'difficult_words': textstat.difficult_words(text),
            'linsear_write_formula': textstat.linsear_write_formula(text),
            'text_standard': textstat.text_standard(text, float_output=True)
        }
        
        return metrics
    
    def analyze_third_party_mentions(self, text):
        """Count mentions of third-party data sharing"""
        if not text:
            return 0
        
        text_lower = text.lower()
        
        # Keywords indicating third-party sharing
        keywords = [
            'third party', 'third-party', 'partners', 'affiliates',
            'share with', 'disclose to', 'sell', 'transfer',
            'advertisers', 'service providers', 'vendors'
        ]
        
        count = sum(text_lower.count(keyword) for keyword in keywords)
        return count
    
    def calculate_read_score(self, metrics):
        """
        Calculate READ(S) component of P6
        Normalize readability scores to 0-1 scale
        Higher score = more readable = better transparency
        """
        if not metrics:
            return 0.0
        
        # Flesch Reading Ease: 0-100 scale (higher is easier)
        # Normalize: divide by 100
        flesch_normalized = max(0, min(100, metrics['flesch_reading_ease'])) / 100
        
        # Grade level: Lower is better (aim for 8th grade or below)
        # Normalize: 1 - (grade_level / 20), cap at grade 20
        grade_level = metrics['flesch_kincaid_grade']
        grade_normalized = max(0, 1 - (min(grade_level, 20) / 20))
        
        # Text standard (overall): Similar to grade level
        text_std = metrics['text_standard']
        text_std_normalized = max(0, 1 - (min(text_std, 20) / 20))
        
        # Average the normalized scores
        read_score = (flesch_normalized + grade_normalized + text_std_normalized) / 3
        
        return round(read_score, 3)
    
    def calculate_third_score(self, third_party_count, text_length):
        """
        Calculate THIRD(S) component of P6
        Based on transparency about third-party sharing
        More mentions = more transparent (up to a point)
        """
        if text_length == 0:
            return 0.0
        
        # Mentions per 1000 words
        words = text_length / 5  # Rough estimate: 5 chars per word
        mentions_per_1000 = (third_party_count / words) * 1000 if words > 0 else 0
        
        # Optimal range: 5-15 mentions per 1000 words
        # Too few = hiding information, too many = repetitive/unclear
        if mentions_per_1000 < 5:
            score = mentions_per_1000 / 5
        elif mentions_per_1000 <= 15:
            score = 1.0
        else:
            score = max(0.5, 1.0 - ((mentions_per_1000 - 15) / 20))
        
        return round(score, 3)
    
    def calculate_p6_score(self, read_score, third_score):
        """
        Calculate P6 (Visibility and Transparency) score
        P6(S) = 0.33·READ(S) + 0.33·LOG(S) + 0.34·THIRD(S)
        
        Note: LOG(S) requires actual user dashboard analysis (not available via policy text)
        So we use: P6(S) = 0.5·READ(S) + 0.5·THIRD(S) for this automated analysis
        """
        # Adjusted weights since we can't measure LOG(S) from policy text
        p6_score = (0.5 * read_score) + (0.5 * third_score)
        
        return round(p6_score, 3)
    
    def analyze_platform(self, platform_name, url):
        """Complete analysis for a single platform"""
        print(f"\n{'='*60}")
        print(f"Analyzing: {platform_name}")
        print(f"URL: {url}")
        print(f"{'='*60}")
        
        # Extract text
        text = self.extract_text_from_url(url)
        
        if not text:
            print(f"❌ Failed to extract text from {platform_name}")
            return None
        
        text_length = len(text)
        word_count = len(text.split())
        
        print(f"✓ Extracted {word_count:,} words ({text_length:,} characters)")
        
        # Readability analysis
        metrics = self.analyze_readability(text)
        
        if not metrics:
            print(f"❌ Failed to analyze readability")
            return None
        
        print(f"✓ Flesch Reading Ease: {metrics['flesch_reading_ease']:.1f}")
        print(f"✓ Grade Level: {metrics['flesch_kincaid_grade']:.1f}")
        print(f"✓ Text Standard: {metrics['text_standard']:.1f}")
        
        # Third-party analysis
        third_party_count = self.analyze_third_party_mentions(text)
        print(f"✓ Third-party mentions: {third_party_count}")
        
        # Calculate scores
        read_score = self.calculate_read_score(metrics)
        third_score = self.calculate_third_score(third_party_count, text_length)
        p6_score = self.calculate_p6_score(read_score, third_score)
        
        print(f"\n📊 SCORES:")
        print(f"   READ(S) - Readability: {read_score:.3f}")
        print(f"   THIRD(S) - Third-party transparency: {third_score:.3f}")
        print(f"   P6 Score - Overall Transparency: {p6_score:.3f}")
        
        result = {
            'Platform': platform_name,
            'URL': url,
            'Analysis_Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Word_Count': word_count,
            'Character_Count': text_length,
            'Flesch_Reading_Ease': round(metrics['flesch_reading_ease'], 2),
            'Flesch_Kincaid_Grade': round(metrics['flesch_kincaid_grade'], 2),
            'Gunning_Fog': round(metrics['gunning_fog'], 2),
            'Text_Standard': round(metrics['text_standard'], 2),
            'Third_Party_Mentions': third_party_count,
            'READ_Score': read_score,
            'THIRD_Score': third_score,
            'P6_Score': p6_score
        }
        
        return result
    
    def analyze_all(self):
        """Analyze all platforms"""
        print("\n" + "="*60)
        print("PRIVACY POLICY TRANSPARENCY ANALYSIS")
        print("="*60)
        
        for platform, url in self.policies.items():
            result = self.analyze_platform(platform, url)
            if result:
                self.results.append(result)
        
        return self.results
    
    def generate_report(self):
        """Generate comparative report"""
        if not self.results:
            print("No results to report")
            return
        
        df = pd.DataFrame(self.results)
        
        print("\n" + "="*60)
        print("COMPARATIVE ANALYSIS REPORT")
        print("="*60)
        
        # Summary table
        print("\n📋 P6 TRANSPARENCY SCORES (0 = Poor, 1 = Excellent):")
        print("-" * 60)
        summary = df[['Platform', 'P6_Score', 'READ_Score', 'THIRD_Score']].copy()
        summary = summary.sort_values('P6_Score', ascending=False)
        print(summary.to_string(index=False))
        
        print("\n📖 READABILITY METRICS:")
        print("-" * 60)
        readability = df[['Platform', 'Flesch_Reading_Ease', 'Flesch_Kincaid_Grade', 'Text_Standard']].copy()
        print(readability.to_string(index=False))
        print("\nNote: Lower grade levels = more readable")
        print("Target: 8th grade level or below for general public")
        
        print("\n🔗 THIRD-PARTY TRANSPARENCY:")
        print("-" * 60)
        third_party = df[['Platform', 'Third_Party_Mentions', 'Word_Count']].copy()
        third_party['Mentions_per_1000_words'] = (third_party['Third_Party_Mentions'] / third_party['Word_Count'] * 1000).round(2)
        print(third_party.to_string(index=False))
        
        print("\n" + "="*60)
        print("INTERPRETATION:")
        print("="*60)
        
        best = summary.iloc[0]
        worst = summary.iloc[-1]
        
        print(f"\n🏆 Best Transparency: {best['Platform']} (P6 = {best['P6_Score']:.3f})")
        print(f"⚠️  Worst Transparency: {worst['Platform']} (P6 = {worst['P6_Score']:.3f})")
        print(f"\n📊 Gap: {(best['P6_Score'] - worst['P6_Score']):.3f}")
        
        avg_score = df['P6_Score'].mean()
        print(f"📈 Average P6 Score: {avg_score:.3f}")
        
        # Classification
        print("\n🎯 PRIVACY BY DESIGN CLASSIFICATION:")
        for _, row in summary.iterrows():
            if row['P6_Score'] >= 0.7:
                classification = "✅ Strong transparency"
            elif row['P6_Score'] >= 0.5:
                classification = "⚠️  Moderate transparency"
            else:
                classification = "❌ Poor transparency"
            print(f"   {row['Platform']}: {classification}")
        
        return df
    
    def save_results(self, filename='privacy_policy_analysis.csv'):
        """Save results to CSV"""
        if not self.results:
            print("No results to save")
            return
        
        df = pd.DataFrame(self.results)
        df.to_csv(filename, index=False)
        print(f"\n💾 Results saved to: {filename}")
        
        # Also save as JSON
        json_filename = filename.replace('.csv', '.json')
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"💾 Results saved to: {json_filename}")


def main():
    """Main execution function"""
    analyzer = PrivacyPolicyAnalyzer()
    
    # Run analysis
    analyzer.analyze_all()
    
    # Generate report
    df = analyzer.generate_report()
    
    # Save results
    analyzer.save_results()
    
    print("\n" + "="*60)
    print("✅ ANALYSIS COMPLETE")
    print("="*60)
    print("\nUse these P6 scores in your PBDIS calculation:")
    print("PBDIS(S) = Σᵢ₌₁⁷ wᵢ · Pᵢ(S)")
    print("where P6 is now quantified for each platform.")


if __name__ == "__main__":
    main()