"""
Dark Patterns Analysis Tool
Manual checklist-based tool for analyzing P7 (Respect for User Privacy)
Based on Mathur et al. (2019) and Gray et al. (2018) taxonomies
"""

import json
from datetime import datetime
import pandas as pd

class DarkPatternsAnalyzer:
    """
    Interactive tool for documenting dark patterns in privacy interfaces
    P7(S) = 1 - DP(S), where DP is dark pattern intensity
    """
    
    def __init__(self):
        self.platforms = ['Meta', 'Google', 'Microsoft', 'Proton']
        
        # Dark pattern taxonomy based on literature
        self.dark_patterns_checklist = {
            'Obstruction': [
                'Privacy settings buried in deep menu hierarchy',
                'Account deletion requires multiple steps/pages',
                'Privacy controls require technical knowledge',
                'No clear path to privacy dashboard',
                'Settings scattered across multiple locations'
            ],
            'Sneaking': [
                'Hidden costs of privacy choices revealed later',
                'Unclear data sharing in fine print',
                'Pre-selected opt-ins disguised as recommendations',
                'Automatic enrollment in data programs',
                'Hidden third-party data sharing'
            ],
            'Interface_Interference': [
                'Privacy-protective option less visually prominent',
                'Manipulative language (e.g., "Don\'t protect me")',
                'Color coding: privacy option in warning colors',
                'Size disparity: privacy option in smaller text',
                'Confirm-shaming: guilt-inducing rejection language'
            ],
            'Forced_Action': [
                'Must accept all data collection to use service',
                'Cannot opt out of tracking without losing features',
                'Requires sharing personal data for basic functionality',
                'No granular privacy controls (all-or-nothing)',
                'Must create account to access privacy settings'
            ],
            'Default_Settings': [
                'Location tracking enabled by default',
                'Ad personalization enabled by default',
                'Data sharing with third parties enabled by default',
                'Activity tracking enabled by default',
                'Cross-service data linking enabled by default'
            ]
        }
        
        self.results = {}
    
    def display_checklist_for_platform(self, platform_name):
        """Display interactive checklist for a platform"""
        print("\n" + "="*70)
        print(f"DARK PATTERNS ANALYSIS: {platform_name}")
        print("="*70)
        print("\nInstructions:")
        print("1. Create a fresh account on the platform")
        print("2. Go through signup flow and privacy settings")
        print("3. Answer YES if the dark pattern is present, NO if absent")
        print("4. Take screenshots as evidence\n")
        
        platform_results = {
            'platform': platform_name,
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'patterns_detected': {},
            'screenshots': []
        }
        
        total_checks = 0
        total_detected = 0
        
        for category, patterns in self.dark_patterns_checklist.items():
            print(f"\n{'─'*70}")
            print(f"📋 Category: {category.replace('_', ' ').upper()}")
            print(f"{'─'*70}")
            
            category_results = []
            
            for i, pattern in enumerate(patterns, 1):
                print(f"\n{i}. {pattern}")
                
                # In a real scenario, you'd answer interactively
                # For demo purposes, we'll provide a template
                response = input("   Present? (y/n or press Enter to skip): ").strip().lower()
                
                is_present = response == 'y'
                
                category_results.append({
                    'pattern': pattern,
                    'detected': is_present
                })
                
                total_checks += 1
                if is_present:
                    total_detected += 1
                    print(f"   ⚠️  DETECTED - Take screenshot and save as:")
                    screenshot_name = f"{platform_name.lower()}_{category.lower()}_{i}.png"
                    print(f"      {screenshot_name}")
                    platform_results['screenshots'].append(screenshot_name)
            
            platform_results['patterns_detected'][category] = category_results
        
        # Calculate scores
        dp_intensity = total_detected / total_checks if total_checks > 0 else 0
        p7_score = 1 - dp_intensity
        
        platform_results['total_patterns_checked'] = total_checks
        platform_results['total_patterns_detected'] = total_detected
        platform_results['dp_intensity'] = round(dp_intensity, 3)
        platform_results['p7_score'] = round(p7_score, 3)
        
        # Category-wise breakdown
        category_scores = {}
        for category, patterns in platform_results['patterns_detected'].items():
            detected = sum(1 for p in patterns if p['detected'])
            total = len(patterns)
            category_scores[category] = {
                'detected': detected,
                'total': total,
                'percentage': round(detected/total * 100, 1) if total > 0 else 0
            }
        
        platform_results['category_breakdown'] = category_scores
        
        print("\n" + "="*70)
        print(f"RESULTS FOR {platform_name}")
        print("="*70)
        print(f"Dark patterns detected: {total_detected}/{total_checks}")
        print(f"DP Intensity: {dp_intensity:.3f}")
        print(f"P7 Score (Respect for User Privacy): {p7_score:.3f}")
        
        print("\n📊 Category Breakdown:")
        for category, scores in category_scores.items():
            print(f"   {category.replace('_', ' ')}: {scores['detected']}/{scores['total']} ({scores['percentage']}%)")
        
        self.results[platform_name] = platform_results
        
        return platform_results
    
    def analyze_all_platforms_batch(self):
        """
        Batch analysis mode - for when you've already collected data
        Enter findings all at once instead of interactively
        """
        print("="*70)
        print("BATCH DARK PATTERNS ANALYSIS")
        print("="*70)
        print("\nThis mode is for when you've already documented dark patterns")
        print("and want to enter the data quickly.\n")
        
        # Example data structure for quick entry
        batch_data = {
            'Meta': {
                'Obstruction': 4,  # Number of patterns detected in this category
                'Sneaking': 4,
                'Interface_Interference': 5,
                'Forced_Action': 3,
                'Default_Settings': 5
            },
            'Google': {
                'Obstruction': 3,
                'Sneaking': 3,
                'Interface_Interference': 4,
                'Forced_Action': 2,
                'Default_Settings': 4
            },
            'Microsoft': {
                'Obstruction': 2,
                'Sneaking': 2,
                'Interface_Interference': 3,
                'Forced_Action': 1,
                'Default_Settings': 3
            },
            'Proton': {
                'Obstruction': 0,
                'Sneaking': 0,
                'Interface_Interference': 0,
                'Forced_Action': 0,
                'Default_Settings': 0
            }
        }
        
        print("Enter detected pattern counts for each category.")
        print("(Press Enter to use example data for quick demo)\n")
        
        use_example = input("Use example data? (y/n): ").strip().lower() == 'y'
        
        if use_example:
            data = batch_data
        else:
            data = {}
            for platform in self.platforms:
                print(f"\n{platform}:")
                platform_data = {}
                for category in self.dark_patterns_checklist.keys():
                    count = input(f"  {category} (0-{len(self.dark_patterns_checklist[category])}): ")
                    platform_data[category] = int(count) if count.strip() else 0
                data[platform] = platform_data
        
        # Process batch data
        for platform, categories in data.items():
            total_detected = sum(categories.values())
            total_possible = sum(len(patterns) for patterns in self.dark_patterns_checklist.values())
            
            dp_intensity = total_detected / total_possible if total_possible > 0 else 0
            p7_score = 1 - dp_intensity
            
            self.results[platform] = {
                'platform': platform,
                'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'total_patterns_checked': total_possible,
                'total_patterns_detected': total_detected,
                'category_detected': categories,
                'dp_intensity': round(dp_intensity, 3),
                'p7_score': round(p7_score, 3)
            }
    
    def generate_report(self):
        """Generate comprehensive dark patterns report"""
        if not self.results:
            print("❌ No analysis results available")
            return
        
        print("\n" + "="*70)
        print("DARK PATTERNS COMPARATIVE ANALYSIS REPORT")
        print("="*70)
        
        # Create summary dataframe
        summary_data = []
        for platform, data in self.results.items():
            summary_data.append({
                'Platform': platform,
                'Patterns_Detected': data['total_patterns_detected'],
                'Patterns_Checked': data['total_patterns_checked'],
                'DP_Intensity': data['dp_intensity'],
                'P7_Score': data['p7_score']
            })
        
        df = pd.DataFrame(summary_data)
        df = df.sort_values('P7_Score', ascending=False)
        
        print("\n📊 P7 SCORES (Respect for User Privacy):")
        print("─"*70)
        print(df.to_string(index=False))
        
        print("\n" + "="*70)
        print("INTERPRETATION:")
        print("="*70)
        
        best = df.iloc[0]
        worst = df.iloc[-1]
        
        print(f"\n🏆 Best (Least manipulative): {best['Platform']}")
        print(f"   P7 Score: {best['P7_Score']:.3f}")
        print(f"   Dark patterns: {best['Patterns_Detected']}/{best['Patterns_Checked']}")
        
        print(f"\n⚠️  Worst (Most manipulative): {worst['Platform']}")
        print(f"   P7 Score: {worst['P7_Score']:.3f}")
        print(f"   Dark patterns: {worst['Patterns_Detected']}/{worst['Patterns_Checked']}")
        
        print(f"\n📈 Gap: {(best['P7_Score'] - worst['P7_Score']):.3f}")
        
        # Classification
        print("\n🎯 PRIVACY RESPECT CLASSIFICATION:")
        for _, row in df.iterrows():
            if row['P7_Score'] >= 0.8:
                classification = "✅ Highly respectful"
            elif row['P7_Score'] >= 0.6:
                classification = "⚠️  Moderately respectful"
            elif row['P7_Score'] >= 0.4:
                classification = "⚠️  Poor respect"
            else:
                classification = "❌ Highly manipulative"
            
            print(f"   {row['Platform']}: {classification}")
        
        # Category analysis
        print("\n📋 DARK PATTERN CATEGORIES (Most Common):")
        if 'category_detected' in list(self.results.values())[0]:
            category_totals = {}
            for platform, data in self.results.items():
                for category, count in data['category_detected'].items():
                    category_totals[category] = category_totals.get(category, 0) + count
            
            sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
            for category, total in sorted_categories:
                print(f"   {category.replace('_', ' ')}: {total} instances across platforms")
        
        return df
    
    def export_results(self, filename='dark_patterns_analysis.json'):
        """Export detailed results"""
        if not self.results:
            print("❌ No results to export")
            return
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Detailed results saved to: {filename}")
        
        # Also export CSV for spreadsheet
        csv_filename = filename.replace('.json', '.csv')
        summary_data = []
        for platform, data in self.results.items():
            summary_data.append({
                'Platform': platform,
                'P7_Score': data['p7_score'],
                'DP_Intensity': data['dp_intensity'],
                'Patterns_Detected': data['total_patterns_detected'],
                'Patterns_Checked': data['total_patterns_checked']
            })
        
        df = pd.DataFrame(summary_data)
        df.to_csv(csv_filename, index=False)
        print(f"💾 Summary saved to: {csv_filename}")
        
        print("\n📋 SCREENSHOT NAMING CONVENTION:")
        print("   Save screenshots as: {platform}_{category}_{number}.png")
        print("   Example: meta_interface_interference_1.png")
        
        return df


def main():
    """Main execution"""
    analyzer = DarkPatternsAnalyzer()
    
    print("="*70)
    print("DARK PATTERNS ANALYSIS TOOL")
    print("="*70)
    print("\nThis tool helps you systematically document dark patterns")
    print("in privacy interfaces to calculate P7 scores.\n")
    
    print("Choose analysis mode:")
    print("1. Interactive (analyze one platform at a time with prompts)")
    print("2. Batch (enter all data at once)")
    
    mode = input("\nSelect mode (1/2): ").strip()
    
    if mode == '1':
        # Interactive mode
        for platform in analyzer.platforms:
            proceed = input(f"\nAnalyze {platform}? (y/n): ").strip().lower()
            if proceed == 'y':
                analyzer.display_checklist_for_platform(platform)
    else:
        # Batch mode (faster for your case study)
        analyzer.analyze_all_platforms_batch()
    
    # Generate report
    analyzer.generate_report()
    
    # Export results
    analyzer.export_results()
    
    print("\n" + "="*70)
    print("✅ DARK PATTERNS ANALYSIS COMPLETE")
    print("="*70)
    print("\nNext steps:")
    print("1. Use P7 scores in your main spreadsheet")
    print("2. Include screenshots in your case study chapter")
    print("3. Reference specific patterns in your analysis")


if __name__ == "__main__":
    main()