"""
Visualization functions for naval mine warfare simulation
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict

# 고품질 시각화 설정
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['savefig.dpi'] = 300


def create_comparison_dashboard(all_results: Dict, output_dir: str):
    """Create comprehensive comparison dashboard"""
    fig, axes = plt.subplots(2, 2, figsize=(18, 14))
    
    threat_names = ['MODERATE', 'HIGH', 'CRITICAL']
    mines = [150, 300, 450]
    
    # 1. Risk comparison bar chart
    ax1 = axes[0, 0]
    surface_risks = [all_results[t]['surface_vessel']['any_hit_prob']*100 for t in threat_names]
    sub_risks = [all_results[t]['submarine']['any_hit_prob']*100 for t in threat_names]
    
    x = np.arange(len(threat_names))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, surface_risks, width, label='Surface Vessel', 
                   color='#3498db', alpha=0.8, edgecolor='black', linewidth=2)
    bars2 = ax1.bar(x + width/2, sub_risks, width, label='Submarine', 
                   color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=2)
    
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{height:.1f}%', ha='center', va='bottom',
                    fontsize=11, fontweight='bold')
    
    ax1.set_ylabel('Risk Probability (%)', fontsize=13, fontweight='bold')
    ax1.set_title('Risk Level Comparison by Threat Level', fontsize=14, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(threat_names)
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3, axis='y')
    ax1.set_ylim(0, max(surface_risks + sub_risks) * 1.15)
    
    # 2. Survival rate trend
    ax2 = axes[0, 1]
    surface_survival = [all_results[t]['surface_vessel']['safe_prob']*100 for t in threat_names]
    sub_survival = [all_results[t]['submarine']['safe_prob']*100 for t in threat_names]
    
    ax2.plot(mines, surface_survival, 'o-', linewidth=3, markersize=12, 
            label='Surface Vessel', color='#3498db', markeredgecolor='black', markeredgewidth=2)
    ax2.plot(mines, sub_survival, 's-', linewidth=3, markersize=12,
            label='Submarine', color='#e74c3c', markeredgecolor='black', markeredgewidth=2)
    
    for i, (m, ss, subs) in enumerate(zip(mines, surface_survival, sub_survival)):
        ax2.text(m, ss + 2, f'{ss:.1f}%', ha='center', fontsize=10, fontweight='bold')
        ax2.text(m, subs - 4, f'{subs:.1f}%', ha='center', fontsize=10, fontweight='bold')
    
    ax2.set_xlabel('Number of Mines', fontsize=13, fontweight='bold')
    ax2.set_ylabel('Survival Rate (%)', fontsize=13, fontweight='bold')
    ax2.set_title('Survival Rate vs Mine Density', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 105)
    
    # 3. Submarine advantage
    ax3 = axes[1, 0]
    advantage = [sub_survival[i] - surface_survival[i] for i in range(3)]
    colors_adv = ['#27ae60' if a > 0 else '#e74c3c' for a in advantage]
    
    bars3 = ax3.bar(threat_names, advantage, color=colors_adv, alpha=0.7, 
                   edgecolor='black', linewidth=2.5)
    
    for bar, adv in zip(bars3, advantage):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + (1 if height > 0 else -3),
                f'{adv:+.1f}%', ha='center', va='bottom' if height > 0 else 'top',
                fontsize=12, fontweight='bold')
    
    ax3.axhline(y=0, color='black', linestyle='--', linewidth=2)
    ax3.set_ylabel('Submarine Advantage (%)', fontsize=13, fontweight='bold')
    ax3.set_title('Submarine Safety Advantage Over Surface', fontsize=14, fontweight='bold')
    ax3.grid(True, alpha=0.3, axis='y')
    
    # 4. Statistics table
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    table_data = []
    for i, threat in enumerate(threat_names):
        surf_risk = all_results[threat]['surface_vessel']['any_hit_prob']*100
        sub_risk = all_results[threat]['submarine']['any_hit_prob']*100
        surf_safe = all_results[threat]['surface_vessel']['safe_prob']*100
        sub_safe = all_results[threat]['submarine']['safe_prob']*100
        
        table_data.append([
            threat,
            f"{mines[i]}",
            f"{surf_risk:.1f}%",
            f"{sub_risk:.1f}%",
            f"{surf_safe:.1f}%",
            f"{sub_safe:.1f}%",
            f"{advantage[i]:+.1f}%"
        ])
    
    table = ax4.table(cellText=table_data,
                     colLabels=['Threat\nLevel', 'Mines', 'Surface\nRisk', 'Sub\nRisk', 
                               'Surface\nSafe', 'Sub\nSafe', 'Sub\nAdvantage'],
                     cellLoc='center',
                     loc='center',
                     bbox=[0, 0.1, 1, 0.8])
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2.5)
    
    for j in range(7):
        cell = table[(0, j)]
        cell.set_facecolor('#2c3e50')
        cell.set_text_props(weight='bold', color='white', fontsize=11)
    
    for i in range(1, len(table_data) + 1):
        for j in range(7):
            cell = table[(i, j)]
            cell.set_facecolor('#ecf0f1' if i % 2 == 0 else 'white')
            cell.set_text_props(fontsize=10)
            
            if j == 6:
                value = float(table_data[i-1][j].replace('%', '').replace('+', ''))
                if value > 0:
                    cell.set_facecolor('#d5f4e6')
                else:
                    cell.set_facecolor('#fadbd8')
    
    ax4.text(0.5, 0.95, 'Comprehensive Statistics Summary', 
            ha='center', va='top', transform=ax4.transAxes,
            fontsize=14, fontweight='bold')
    
    plt.suptitle('Tactical Mine Warfare Simulation - Comprehensive Analysis Dashboard', 
                fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    
    save_path = f'{output_dir}/comparison_dashboard.png'
    plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"\n✓ Saved: comparison_dashboard.png")