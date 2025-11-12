"""
Default Privacy Settings Auditor
Calculates P2 (Privacy as Default) scores
Based on out-of-the-box privacy settings configuration
"""

import json
from datetime import datetime
import pandas as pd

class DefaultSettingsAuditor:
    """
    Audits default privacy settings to calculate P2 scores
    P2(S) = N_restrictive / N_total
    """
    
    def __init__(self):
        self.platforms = ['Meta', 'Google', 'Microsoft', 'Proton']
        
        # Standard privacy settings to check across platforms
        self.settings_checklist = {
            'Data Collection': [
                'Location tracking',
                'Browsing history collection',
                'Search history collection',
                'Contact access',
                'Photo/media access',
                'Microphone access',
                'Camera access'
            ],
            'Advertising & Personalization': [
                'Personalized ads',
                'Ad tracking across apps/sites',
                'Interest-based advertising',
                'Advertiser data sharing',
                'Marketing communications'
            ],
            'Data Sharing': [
                'Share data with third parties',
                'Share data with partners/affiliates',
                'Cross-service data linking',
                'Public profile visibility',
                'Search engine indexing'
            ],
            'Account Activity': [
                'Activity/usage tracking',
                'Purchase history tracking',
                'Voice recordings storage',
                'Face recognition',
                'Biometric data collection'
            ],
            'Communications': [
                'Email read receipts',
                'Online status visibility',
                'Last seen timestamp',
                'Message preview in notifications',
                'Contact sync'
            ]
        }
        
        self.results = {}
    
    def audit_platform_interactive(self, platform_name):
        """Interactive audit for a single platform"""
        print("\n" + "="*70)
        print(f"DEFAULT SETTINGS AUDIT: {platform_name}")
        print("="*70)
        print("\nInstructions:")
        print("1. Create a FRESH account (or use incognito mode)")
        print("2. Do NOT change any settings during signup")
        print("3. Navigate to privacy/settings page")
        print("4. For each setting, note if it's:")
        print("   - ON (data collection enabled) = Privacy-invasive default")
        print("   - OFF (data collection disabled) = Privacy-protective default")
        print("   - N/A (setting doesn't exist on this platform)\n")
        
        platform_results = {
            'platform': platform_name,
            'audit_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'settings': {},
            'screenshots': []
        }
        
        total_settings = 0
        restrictive_defaults = 0  # Privacy-protective (good)
        
        for category, settings in self.settings_checklist.items():
            print(f"\n{'─'*70}")
            print(f"📋 {category}")
            print(f"{'─'*70}")
            
            category_results = []
            
            for i, setting in enumerate(settings, 1):
                print(f"\n{i}. {setting}")
                print("   Default status?")
                print("   [1] ON (collecting data) - Privacy-invasive")
                print("   [2] OFF (not collecting) - Privacy-protective ✓")
                print("   [3] N/A (doesn't exist)")
                
                response = input("   Select (1/2/3): ").strip()
                
                if response == '3':
                    # Setting doesn't exist, skip it
                    continue
                
                is_restrictive = response == '2'  # OFF = good for privacy
                
                category_results.append({
                    'setting': setting,
                    'default_status': 'OFF' if is_restrictive else 'ON',
                    'privacy_protective': is_restrictive
                })
                
                total_settings += 1
                if is_restrictive:
                    restrictive_defaults += 1
                    print("   ✓ Privacy-protective default")
                else:
                    print("   ⚠️ Privacy-invasive default")
                
                # Suggest screenshot
                if not is_restrictive:
                    screenshot_name = f"{platform_name.lower()}_default_{category.lower().replace(' ', '_')}_{i}.png"
                    print(f"   📸 Screenshot: {screenshot_name}")
                    platform_results['screenshots'].append(screenshot_name)
            
            if category_results:
                platform_results['settings'][category] = category_results
        
        # Calculate P2 score
        p2_score = restrictive_defaults / total_settings if total_settings > 0 else 0
        
        platform_results['total_settings_checked'] = total_settings
        platform_results['privacy_protective_defaults'] = restrictive_defaults
        platform_results['privacy_invasive_defaults'] = total_settings - restrictive_defaults
        platform_results['p2_score'] = round(p2_score, 3)
        
        print("\n" + "="*70)
        print(f"RESULTS FOR {platform_name}")
        print("="*70)
        print(f"Total settings checked: {total_settings}")
        print(f"Privacy-protective defaults: {restrictive_defaults}")
        print(f"Privacy-invasive defaults: {total_settings - restrictive_defaults}")
        print(f"\nP2 Score (Privacy as Default): {p2_score:.3f}")
        
        # Category breakdown
        print("\n📊 Category Breakdown:")
        for category, settings_list in platform_results['settings'].items():
            protective = sum(1 for s in settings_list if s['privacy_protective'])
            total = len(settings_list)
            print(f"   {category}: {protective}/{total} privacy-protective")
        
        self.results[platform_name] = platform_results
        
        return platform_results
    
    def audit_batch_mode(self):
        """
        Batch mode - enter all data at once
        Useful when you've already documented settings
        """
        print("="*70)
        print("BATCH DEFAULT SETTINGS AUDIT")
        print("="*70)
        print("\nEnter the number of privacy-PROTECTIVE defaults (OFF by default)")
        print("for each platform.\n")
        
        # Example data based on typical platform behaviors
        example_data = {
            'Meta': {
                'Data Collection': 1,  # Most tracking ON by default
                'Advertising & Personalization': 0,
                'Data Sharing': 0,
                'Account Activity': 0,
                'Communications': 2
            },
            'Google': {
                'Data Collection': 1,
                'Advertising & Personalization': 1,
                'Data Sharing': 0,
                'Account Activity': 1,
                'Communications': 2
            },
            'Microsoft': {
                'Data Collection': 2,
                'Advertising & Personalization': 2,
                'Data Sharing': 1,
                'Account Activity': 2,
                'Communications': 3
            },
            'Proton': {
                'Data Collection': 7,  # Minimal tracking, most OFF
                'Advertising & Personalization': 5,
                'Data Sharing': 5,
                'Account Activity': 5,
                'Communications': 5
            }
        }
        
        use_example = input("Use example data for quick demo? (y/n): ").strip().lower() == 'y'
        
        if use_example:
            data = example_data
        else:
            data = {}
            for platform in self.platforms:
                print(f"\n{platform}:")
                platform_data = {}
                for category, settings in self.settings_checklist.items():
                    count = input(f"  {category} - Privacy-protective (0-{len(settings)}): ")
                    platform_data[category] = int(count) if count.strip() else 0
                data[platform] = platform_data
        
        # Process batch data
        for platform, categories in data.items():
            total_protective = sum(categories.values())
            total_possible = sum(len(settings) for settings in self.settings_checklist.values())
            
            p2_score = total_protective / total_possible if total_possible > 0 else 0
            
            self.results[platform] = {
                'platform': platform,
                'audit_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'total_settings_checked': total_possible,
                'privacy_protective_defaults': total_protective,
                'privacy_invasive_defaults': total_possible - total_protective,
                'category_breakdown': categories,
                'p2_score': round(p2_score, 3)
            }
    
    def generate_report(self):
        """Generate comparative report"""
        if not self.results:
            print("❌ No audit results available")
            return
        
        print("\n" + "="*70)
        print("DEFAULT PRIVACY SETTINGS COMPARATIVE REPORT")
        print("="*70)
        
        # Create summary dataframe
        summary_data = []
        for platform, data in self.results.items():
            summary_data.append({
                'Platform': platform,
                'Total_Settings': data['total_settings_checked'],
                'Privacy_Protective': data['privacy_protective_defaults'],
                'Privacy_Invasive': data['privacy_invasive_defaults'],
                'P2_Score': data['p2_score'],
                'Percentage': f"{data['p2_score']*100:.1f}%"
            })
        
        df = pd.DataFrame(summary_data)
        df = df.sort_values('P2_Score', ascending=False)
        
        print("\n📊 P2 SCORES (Privacy as Default):")
        print("─"*70)
        print(df.to_string(index=False))
        
        print("\n" + "="*70)
        print("INTERPRETATION:")
        print("="*70)
        
        best = df.iloc[0]
        worst = df.iloc[-1]
        
        print(f"\n🏆 Best (Privacy by Default): {best['Platform']}")
        print(f"   P2 Score: {best['P2_Score']:.3f}")
        print(f"   Privacy-protective: {best['Privacy_Protective']}/{best['Total_Settings']}")
        
        print(f"\n⚠️  Worst (Surveillance by Default): {worst['Platform']}")
        print(f"   P2 Score: {worst['P2_Score']:.3f}")
        print(f"   Privacy-protective: {worst['Privacy_Protective']}/{worst['Total_Settings']}")
        
        print(f"\n📈 Gap: {(best['P2_Score'] - worst['P2_Score']):.3f}")
        
        avg_score = df['P2_Score'].mean()
        print(f"📊 Average P2 Score: {avg_score:.3f}")
        
        # Classification
        print("\n🎯 PRIVACY BY DEFAULT CLASSIFICATION:")
        for _, row in df.iterrows():
            if row['P2_Score'] >= 0.8:
                classification = "✅ Excellent - True Privacy by Default"
            elif row['P2_Score'] >= 0.6:
                classification = "✓ Good - Mostly privacy-protective"
            elif row['P2_Score'] >= 0.4:
                classification = "⚠️  Poor - Mostly invasive defaults"
            else:
                classification = "❌ Terrible - Surveillance by Default"
            
            print(f"   {row['Platform']}: {classification}")
        
        # Category analysis (if available)
        print("\n📋 CATEGORY ANALYSIS:")
        if 'category_breakdown' in list(self.results.values())[0]:
            for category in self.settings_checklist.keys():
                print(f"\n   {category}:")
                for platform, data in self.results.items():
                    if 'category_breakdown' in data:
                        count = data['category_breakdown'].get(category, 0)
                        total = len(self.settings_checklist[category])
                        pct = (count/total)*100 if total > 0 else 0
                        print(f"      {platform}: {count}/{total} ({pct:.0f}%)")
        
        print("\n💡 KEY INSIGHT:")
        print("   P2 directly measures compliance with GDPR Article 25(2):")
        print("   'Privacy by default' principle requires privacy-protective")
        print("   settings without user intervention.")
        
        return df
    
    def export_results(self, filename='default_settings_audit.json'):
        """Export detailed results"""
        if not self.results:
            print("❌ No results to export")
            return
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Detailed results saved to: {filename}")
        
        # Export CSV
        csv_filename = filename.replace('.json', '.csv')
        summary_data = []
        for platform, data in self.results.items():
            summary_data.append({
                'Platform': platform,
                'P2_Score': data['p2_score'],
                'Privacy_Protective': data['privacy_protective_defaults'],
                'Privacy_Invasive': data['privacy_invasive_defaults'],
                'Total_Settings': data['total_settings_checked']
            })
        
        df = pd.DataFrame(summary_data)
        df.to_csv(csv_filename, index=False)
        print(f"💾 Summary saved to: {csv_filename}")
        
        return df


def main():
    """Main execution"""
    auditor = DefaultSettingsAuditor()
    
    print("="*70)
    print("DEFAULT PRIVACY SETTINGS AUDITOR")
    print("="*70)
    print("\nThis tool calculates P2 (Privacy as Default) scores")
    print("by auditing out-of-the-box privacy settings.\n")
    
    print("Choose audit mode:")
    print("1. Interactive (audit one platform at a time)")
    print("2. Batch (enter all data at once) - RECOMMENDED for speed")
    
    mode = input("\nSelect mode (1/2): ").strip()
    
    if mode == '1':
        # Interactive mode
        for platform in auditor.platforms:
            proceed = input(f"\nAudit {platform}? (y/n): ").strip().lower()
            if proceed == 'y':
                auditor.audit_platform_interactive(platform)
    else:
        # Batch mode (faster)
        auditor.audit_batch_mode()
    
    # Generate report
    auditor.generate_report()
    
    # Export results
    auditor.export_results()
    
    print("\n" + "="*70)
    print("✅ DEFAULT SETTINGS AUDIT COMPLETE")
    print("="*70)
    print("\nNext steps:")
    print("1. Use P2 scores in your main PBDIS calculation")
    print("2. Include screenshots of invasive defaults as evidence")
    print("3. Reference specific settings in your analysis")


if __name__ == "__main__":
    main()