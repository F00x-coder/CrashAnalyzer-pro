#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.font_manager as fm
import numpy as np
import pandas as pd
import json
import os
from datetime import datetime
import threading
import time

# Configure fonts for better rendering
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']

class ElegantCrashAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Ghost Crash Analyzer Pro")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1a1a2e')
        
        # Load data
        self.history = []
        self.session_profit = 0
        self.predictions = []
        self.risk_level = "Medium"
        self.load_data()
        
        # Setup interface
        self.setup_styles()
        self.setup_gui()
        self.update_dashboard()
        
        # Start auto-update
        self.auto_update()
    
    def setup_styles(self):
        """Setup styles and formatting"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Custom styles
        self.style.configure('Title.TLabel', background='#1a1a2e', foreground='#00b4d8', 
                           font=('Arial', 24, 'bold'))
        self.style.configure('Card.TFrame', background='#16213e', relief='raised', borderwidth=2)
        self.style.configure('Stats.TLabel', background='#16213e', foreground='#e6e6e6', 
                           font=('Arial', 12))
        self.style.configure('Accent.TButton', background='#00b4d8', foreground='white', 
                           font=('Arial', 11, 'bold'), focuscolor='none')
    
    def setup_gui(self):
        """Create main interface"""
        # Create tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Dashboard tab
        self.dashboard_tab = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(self.dashboard_tab, text="🏠 Dashboard")
        
        # Quick input tab
        self.quick_input_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.quick_input_tab, text="⚡ Quick Input")
        
        # Advanced analysis tab
        self.analysis_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.analysis_tab, text="📊 Advanced Analysis")
        
        # Charts tab
        self.charts_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.charts_tab, text="📈 Charts")
        
        # Settings tab
        self.settings_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_tab, text="⚙️ Settings")
        
        # Setup each tab
        self.setup_dashboard()
        self.setup_quick_input()
        self.setup_analysis_tab()
        self.setup_charts_tab()
        self.setup_settings_tab()
    
    def setup_dashboard(self):
        """Setup main dashboard"""
        # Main title
        title_frame = ttk.Frame(self.dashboard_tab)
        title_frame.pack(fill='x', padx=20, pady=20)
        
        title_label = ttk.Label(title_frame, text="🎯 Ghost Crash Analyzer Pro", 
                               style='Title.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, text="Intelligent Crash Game Analysis System", 
                                  background='#1a1a2e', foreground='#8ecae6', 
                                  font=('Arial', 14))
        subtitle_label.pack(pady=5)
        
        # Statistics cards
        self.stats_cards_frame = ttk.Frame(self.dashboard_tab)
        self.stats_cards_frame.pack(fill='x', padx=20, pady=10)
        
        # Cards will be created dynamically in update_dashboard
        
        # Quick actions area
        actions_frame = ttk.LabelFrame(self.dashboard_tab, text="🚀 Quick Actions", padding=15)
        actions_frame.pack(fill='x', padx=20, pady=20)
        
        quick_actions = [
            ("➕ Add New Data", self.show_quick_input),
            ("🎯 Quick Prediction", self.quick_prediction),
            ("📊 Full Analysis", self.run_full_analysis),
            ("📈 Show Chart", self.show_charts),
            ("💾 Save Data", self.save_data),
            ("🔄 Refresh", self.update_dashboard)
        ]
        
        actions_row1 = ttk.Frame(actions_frame)
        actions_row1.pack(fill='x', pady=10)
        actions_row2 = ttk.Frame(actions_frame)
        actions_row2.pack(fill='x', pady=10)
        
        for i, (text, command) in enumerate(quick_actions):
            btn = tk.Button(actions_row1 if i < 3 else actions_row2, text=text, 
                          command=command, bg='#00b4d8', fg='white', 
                          font=('Arial', 11, 'bold'), relief='raised', bd=3, 
                          width=20, height=2)
            btn.pack(side='left', expand=True, padx=10)
        
        # Live predictions area
        self.live_predictions_frame = ttk.LabelFrame(self.dashboard_tab, 
                                                   text="🔮 Live Predictions", padding=15)
        self.live_predictions_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.predictions_text = scrolledtext.ScrolledText(self.live_predictions_frame, 
                                                        height=8, font=('Arial', 10), 
                                                        bg='#1a1a2e', fg='#e6e6e6')
        self.predictions_text.pack(fill='both', expand=True)
    
    def create_stat_card(self, parent, title, value, color, icon):
        """Create statistical card"""
        card = tk.Frame(parent, bg='#16213e', relief='raised', bd=2)
        
        # Icon
        icon_label = tk.Label(card, text=icon, font=('Arial', 20), 
                            bg='#16213e', fg=color)
        icon_label.pack(side='left', padx=10)
        
        # Content
        content_frame = tk.Frame(card, bg='#16213e')
        content_frame.pack(side='left', fill='both', expand=True, padx=5, pady=10)
        
        title_label = tk.Label(content_frame, text=title, bg='#16213e', 
                             fg='#8ecae6', font=('Arial', 10))
        title_label.pack(anchor='w')
        
        value_label = tk.Label(content_frame, text=value, bg='#16213e', 
                             fg='white', font=('Arial', 16, 'bold'))
        value_label.pack(anchor='w')
        
        return card, value_label
    
    def setup_quick_input(self):
        """Setup quick input tab"""
        main_frame = tk.Frame(self.quick_input_tab, bg='#1a1a2e')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="⚡ Quick Data Input", 
                              font=('Arial', 18, 'bold'), bg='#1a1a2e', fg='#00b4d8')
        title_label.pack(pady=10)
        
        # Input frame
        input_frame = tk.Frame(main_frame, bg='#16213e', relief='raised', bd=2)
        input_frame.pack(fill='x', pady=20)
        
        tk.Label(input_frame, text="Enter crash point:", font=('Arial', 14), 
                bg='#16213e', fg='#e6e6e6').pack(pady=10)
        
        self.quick_entry = tk.Entry(input_frame, font=('Arial', 16), width=15, 
                                  justify='center', bg='#2a2a4e', fg='white', 
                                  insertbackground='white')
        self.quick_entry.pack(pady=10)
        self.quick_entry.bind('<Return>', lambda e: self.quick_add_point())
        
        # Input buttons
        buttons_frame = tk.Frame(input_frame, bg='#16213e')
        buttons_frame.pack(pady=15)
        
        add_btn = tk.Button(buttons_frame, text="➕ Add Point", 
                          command=self.quick_add_point, font=('Arial', 12, 'bold'), 
                          bg='#27AE60', fg='white', width=15, height=2)
        add_btn.pack(side='left', padx=10)
        
        bulk_btn = tk.Button(buttons_frame, text="📥 Bulk Add", 
                           command=self.bulk_input, font=('Arial', 12), 
                           bg='#3498DB', fg='white', width=15, height=2)
        bulk_btn.pack(side='left', padx=10)
        
        clear_btn = tk.Button(buttons_frame, text="🗑️ Clear History", 
                            command=self.clear_history, font=('Arial', 12), 
                            bg='#E74C3C', fg='white', width=15, height=2)
        clear_btn.pack(side='left', padx=10)
        
        # Recent data display
        recent_frame = tk.LabelFrame(main_frame, text="📋 Recently Added Points", 
                                   bg='#1a1a2e', fg='#00b4d8', 
                                   font=('Arial', 12, 'bold'))
        recent_frame.pack(fill='both', expand=True, pady=10)
        
        self.recent_text = scrolledtext.ScrolledText(recent_frame, height=10, 
                                                   font=('Arial', 11), 
                                                   bg='#16213e', fg='#e6e6e6')
        self.recent_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def setup_analysis_tab(self):
        """Setup advanced analysis tab"""
        main_frame = tk.Frame(self.analysis_tab, bg='#1a1a2e')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="📊 Advanced Analysis", 
                              font=('Arial', 18, 'bold'), bg='#1a1a2e', fg='#00b4d8')
        title_label.pack(pady=10)
        
        # Analysis buttons
        analysis_buttons_frame = tk.Frame(main_frame, bg='#1a1a2e')
        analysis_buttons_frame.pack(fill='x', pady=20)
        
        analysis_types = [
            ("🎯 Statistical Analysis", self.statistical_analysis),
            ("📈 Trend Analysis", self.trend_analysis),
            ("⚡ Quick Analysis", self.quick_analysis),
            ("🔍 Pattern Analysis", self.pattern_analysis),
            ("💰 Profit Analysis", self.profitability_analysis),
            ("🎲 Probability Analysis", self.probability_analysis)
        ]
        
        for i, (text, command) in enumerate(analysis_types):
            row = i // 3
            col = i % 3
            btn = tk.Button(analysis_buttons_frame, text=text, command=command, 
                          font=('Arial', 11), bg='#9B59B6', fg='white', 
                          width=20, height=2)
            btn.grid(row=row, column=col, padx=10, pady=10, sticky='ew')
        
        # Results area
        results_frame = tk.LabelFrame(main_frame, text="📋 Analysis Results", 
                                    bg='#1a1a2e', fg='#00b4d8', 
                                    font=('Arial', 12, 'bold'))
        results_frame.pack(fill='both', expand=True, pady=10)
        
        self.analysis_text = scrolledtext.ScrolledText(results_frame, height=15, 
                                                     font=('Arial', 11), 
                                                     bg='#16213e', fg='#e6e6e6')
        self.analysis_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def setup_charts_tab(self):
        """Setup charts tab"""
        main_frame = tk.Frame(self.charts_tab, bg='#1a1a2e')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="📈 Interactive Charts", 
                              font=('Arial', 18, 'bold'), bg='#1a1a2e', fg='#00b4d8')
        title_label.pack(pady=10)
        
        # Chart buttons
        chart_buttons_frame = tk.Frame(main_frame, bg='#1a1a2e')
        chart_buttons_frame.pack(fill='x', pady=20)
        
        chart_types = [
            ("📊 Points Chart", self.plot_points_chart),
            ("📈 Moving Average", self.plot_moving_average),
            ("📉 Trend Analysis", self.plot_trend_analysis),
            ("📊 Distribution", self.plot_distribution),
            ("💰 Profit Trend", self.plot_profit_trend),
            ("🎯 Risk Analysis", self.plot_risk_analysis)
        ]
        
        for i, (text, command) in enumerate(chart_types):
            btn = tk.Button(chart_buttons_frame, text=text, command=command, 
                          font=('Arial', 10), bg='#3498DB', fg='white', 
                          width=18, height=2)
            btn.pack(side='left', expand=True, padx=5)
        
        # Chart frame
        self.chart_frame = tk.Frame(main_frame, bg='white', relief='sunken', bd=2)
        self.chart_frame.pack(fill='both', expand=True, pady=10)
    
    def setup_settings_tab(self):
        """Setup settings tab"""
        main_frame = tk.Frame(self.settings_tab, bg='#1a1a2e')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="⚙️ System Settings", 
                              font=('Arial', 18, 'bold'), bg='#1a1a2e', fg='#00b4d8')
        title_label.pack(pady=10)
        
        # Settings frame
        settings_frame = tk.Frame(main_frame, bg='#16213e', relief='raised', bd=2)
        settings_frame.pack(fill='both', expand=True, pady=20)
        
        # Analysis settings
        analysis_settings = tk.LabelFrame(settings_frame, text="Analysis Settings", 
                                        bg='#16213e', fg='#8ecae6', 
                                        font=('Arial', 12, 'bold'))
        analysis_settings.pack(fill='x', padx=20, pady=10)
        
        tk.Label(analysis_settings, text="Analysis window size:", 
                bg='#16213e', fg='white', font=('Arial', 10)).pack(side='left', 
                padx=10, pady=10)
        
        self.window_size = tk.StringVar(value="10")
        window_combo = ttk.Combobox(analysis_settings, textvariable=self.window_size, 
                                  values=["5", "10", "15", "20", "25"], 
                                  state="readonly", width=10)
        window_combo.pack(side='left', padx=10, pady=10)
        
        # Data settings
        data_settings = tk.LabelFrame(settings_frame, text="Data Management", 
                                    bg='#16213e', fg='#8ecae6', 
                                    font=('Arial', 12, 'bold'))
        data_settings.pack(fill='x', padx=20, pady=10)
        
        data_buttons = [
            ("💾 Save Data", self.save_data),
            ("📥 Export Data", self.export_data),
            ("📤 Import Data", self.import_data),
            ("🗑️ Clear All", self.clear_all_data)
        ]
        
        data_buttons_frame = tk.Frame(data_settings, bg='#16213e')
        data_buttons_frame.pack(fill='x', pady=10)
        
        for text, command in data_buttons:
            btn = tk.Button(data_buttons_frame, text=text, command=command, 
                          font=('Arial', 10), bg='#34495E', fg='white', width=15)
            btn.pack(side='left', expand=True, padx=5)
        
        # UI settings
        ui_settings = tk.LabelFrame(settings_frame, text="Interface Settings", 
                                  bg='#16213e', fg='#8ecae6', 
                                  font=('Arial', 12, 'bold'))
        ui_settings.pack(fill='x', padx=20, pady=10)
        
        self.auto_update_var = tk.BooleanVar(value=True)
        auto_update_cb = tk.Checkbutton(ui_settings, text="Auto Update", 
                                      variable=self.auto_update_var, 
                                      bg='#16213e', fg='white', 
                                      selectcolor='#16213e')
        auto_update_cb.pack(side='left', padx=10, pady=10)
        
        # System info
        info_frame = tk.LabelFrame(settings_frame, text="System Information", 
                                 bg='#16213e', fg='#8ecae6', 
                                 font=('Arial', 12, 'bold'))
        info_frame.pack(fill='x', padx=20, pady=10)
        
        info_text = f"""
Software Version: Ghost Crash Analyzer Pro v2.0
Loaded Points: {len(self.history)}
Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M')}
System Status: ✅ Active
"""
        info_label = tk.Label(info_frame, text=info_text, bg='#16213e', 
                            fg='#e6e6e6', font=('Arial', 10), justify='left')
        info_label.pack(padx=10, pady=10)
    
    def update_dashboard(self):
        """Update dashboard"""
        # Clear old cards
        for widget in self.stats_cards_frame.winfo_children():
            widget.destroy()
        
        # Create new cards
        stats_data = [
            ("Total Points", f"{len(self.history)}", "#27AE60", "📊"),
            ("Default Profit", f"{self.session_profit:.2f} 💰", "#3498DB", "💰"),
            ("Win Rate", f"{self.calculate_win_rate():.1f}%", "#9B59B6", "📈"),
            ("Highest Value", f"{max(self.history) if self.history else 0:.2f}x", "#E74C3C", "🚀"),
            ("Lowest Value", f"{min(self.history) if self.history else 0:.2f}x", "#F39C12", "📉"),
            ("Volatility", f"{self.calculate_volatility():.3f}", "#1ABC9C", "⚡")
        ]
        
        self.stat_cards = []
        for i, (title, value, color, icon) in enumerate(stats_data):
            row = i // 3
            col = i % 3
            card_frame = tk.Frame(self.stats_cards_frame, bg='#1a1a2e')
            card_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            card, value_label = self.create_stat_card(card_frame, title, value, color, icon)
            card.pack(fill='both', expand=True)
            self.stat_cards.append((card, value_label))
        
        # Update live predictions
        self.update_live_predictions()
        
        # Update recent data
        self.update_recent_data()
    
    def update_live_predictions(self):
        """Update live predictions"""
        self.predictions_text.config(state='normal')
        self.predictions_text.delete(1.0, tk.END)
        
        if len(self.history) < 3:
            self.predictions_text.insert(1.0, "Add at least 3 points for prediction...")
        else:
            prediction = self.smart_prediction()
            risk = self.risk_analysis()
            signals = self.trading_signals()
            
            predictions_text = f"""
🎯 Smart Prediction: {prediction}
⚠️ Risk Level: {risk['level']} {risk['icon']}
📊 Volatility: {risk['volatility']:.3f}
🚦 Trading Signals: {signals}
💡 Recommendations: {risk['recommendation']}
"""
            self.predictions_text.insert(1.0, predictions_text)
        
        self.predictions_text.config(state='disabled')
    
    def update_recent_data(self):
        """Update recent data"""
        self.recent_text.config(state='normal')
        self.recent_text.delete(1.0, tk.END)
        
        if not self.history:
            self.recent_text.insert(1.0, "No data added yet...")
        else:
            recent_data = "📋 Recently Added Points:\n\n"
            for i, point in enumerate(self.history[-10:][::-1], 1):  # Show last 10 points
                profit = (point - 1) * 10 if point > 1 else -10
                trend = "📈" if i > 1 and point > self.history[-i] else "📉"
                recent_data += f"{trend} Point {len(self.history)-i+1}: {point:.2f}x | Profit: {profit:+.2f}\n"
            
            self.recent_text.insert(1.0, recent_data)
        
        self.recent_text.config(state='disabled')
    
    def quick_add_point(self):
        """Quick add point"""
        point_str = self.quick_entry.get().strip()
        if not point_str:
            messagebox.showwarning("Warning", "Please enter a crash point")
            return
        
        try:
            point = float(point_str)
            if point <= 0:
                messagebox.showwarning("Warning", "Point must be greater than zero")
                return
            
            self.history.append(point)
            
            # Calculate profit
            if point > 1.0:
                profit = (point - 1) * 10
                self.session_profit += profit
                messagebox.showinfo("Success", f"✅ Point added: {point}x\n💰 Profit: +{profit:.2f}")
            else:
                messagebox.showinfo("Success", f"✅ Point added: {point}x\n💸 Complete loss")
            
            self.quick_entry.delete(0, tk.END)
            self.save_data()
            self.update_dashboard()
            
        except ValueError:
            messagebox.showerror("Error", "❌ Please enter a valid number")
    
    # Analysis methods (to be implemented)
    def calculate_win_rate(self):
        """Calculate win rate"""
        if not self.history:
            return 0
        wins = len([x for x in self.history if x > 1.0])
        return (wins / len(self.history)) * 100
    
    def calculate_volatility(self):
        """Calculate volatility"""
        if len(self.history) < 2:
            return 0
        return np.std(self.history)
    
    def smart_prediction(self):
        """Smart prediction algorithm"""
        if len(self.history) < 3:
            return "N/A"
        recent = self.history[-5:]
        prediction = np.mean(recent) * 1.1
        return f"{max(1.01, prediction):.2f}x"
    
    def risk_analysis(self):
        """Risk analysis"""
        if len(self.history) < 3:
            return {"level": "Low", "icon": "🟢", "volatility": 0, "recommendation": "Add more data"}
        
        volatility = self.calculate_volatility()
        if volatility < 0.5:
            return {"level": "Low", "icon": "🟢", "volatility": volatility, "recommendation": "Safe to bet"}
        elif volatility < 1.0:
            return {"level": "Medium", "icon": "🟡", "volatility": volatility, "recommendation": "Bet with caution"}
        else:
            return {"level": "High", "icon": "🔴", "volatility": volatility, "recommendation": "Avoid betting"}
    
    def trading_signals(self):
        """Trading signals"""
        if len(self.history) < 3:
            return "N/A"
        prediction = float(self.smart_prediction().replace('x', ''))
        if prediction > 2.5:
            return "🟢 STRONG BUY"
        elif prediction > 1.8:
            return "🟡 MODERATE BUY"
        else:
            return "🔴 AVOID"
    
    def show_quick_input(self):
        """Show quick input tab"""
        self.notebook.select(1)
    
    def show_charts(self):
        """Show charts tab"""
        self.notebook.select(3)
    
    def quick_prediction(self):
        """Quick prediction"""
        if len(self.history) < 3:
            messagebox.showinfo("Prediction", "Add at least 3 points for prediction")
        else:
            prediction = self.smart_prediction()
            messagebox.showinfo("Quick Prediction", f"Next round: {prediction}")
    
    def run_full_analysis(self):
        """Run full analysis"""
        self.statistical_analysis()
    
    def statistical_analysis(self):
        """Statistical analysis"""
        self.analysis_text.config(state='normal')
        self.analysis_text.delete(1.0, tk.END)
        
        if len(self.history) < 3:
            self.analysis_text.insert(1.0, "Add at least 3 points for analysis")
        else:
            analysis = f"""
📊 Statistical Analysis Report
{'='*40}

Basic Statistics:
├─ Total Points: {len(self.history)}
├─ Mean: {np.mean(self.history):.3f}x
├─ Median: {np.median(self.history):.3f}x
├─ Standard Deviation: {np.std(self.history):.3f}
├─ Variance: {np.var(self.history):.3f}
└─ Range: {max(self.history) - min(self.history):.3f}

Performance Metrics:
├─ Win Rate: {self.calculate_win_rate():.1f}%
├─ Profit Factor: {(self.session_profit/len(self.history)):.3f}
└─ Risk/Reward Ratio: {(np.mean(self.history)/np.std(self.history)):.3f}

Distribution Analysis:
├─ Skewness: {self.calculate_skewness():.3f}
├─ Kurtosis: {self.calculate_kurtosis():.3f}
└─ Volatility Index: {self.calculate_volatility():.3f}
"""
            self.analysis_text.insert(1.0, analysis)
        
        self.analysis_text.config(state='disabled')
    
    def calculate_skewness(self):
        """Calculate skewness"""
        if len(self.history) < 3:
            return 0
        return float(pd.Series(self.history).skew())
    
    def calculate_kurtosis(self):
        """Calculate kurtosis"""
        if len(self.history) < 4:
            return 0
        return float(pd.Series(self.history).kurtosis())
    
    def trend_analysis(self):
        """Trend analysis"""
        self.analysis_text.config(state='normal')
        self.analysis_text.delete(1.0, tk.END)
        
        if len(self.history) < 5:
            self.analysis_text.insert(1.0, "Add at least 5 points for trend analysis")
        else:
            # Implement trend analysis logic
            analysis = "📈 Trend Analysis - Feature coming soon!"
            self.analysis_text.insert(1.0, analysis)
        
        self.analysis_text.config(state='disabled')
    
    def quick_analysis(self):
        """Quick analysis"""
        self.statistical_analysis()
    
    def pattern_analysis(self):
        """Pattern analysis"""
        self.analysis_text.config(state='normal')
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(1.0, "🔍 Pattern Analysis - Feature coming soon!")
        self.analysis_text.config(state='disabled')
    
    def profitability_analysis(self):
        """Profitability analysis"""
        self.analysis_text.config(state='normal')
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(1.0, "💰 Profitability Analysis - Feature coming soon!")
        self.analysis_text.config(state='disabled')
    
    def probability_analysis(self):
        """Probability analysis"""
        self.analysis_text.config(state='normal')
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(1.0, "🎲 Probability Analysis - Feature coming soon!")
        self.analysis_text.config(state='disabled')
    
    # Chart methods
    def plot_points_chart(self):
        """Plot points chart"""
        self.clear_chart_frame()
        if len(self.history) < 2:
            messagebox.showwarning("Warning", "Add at least 2 points for chart")
            return
        
        fig, ax = plt.subplots(figsize=(10, 6), facecolor='#1a1a2e')
        ax.set_facecolor('#1a1a2e')
        
        points = self.history[-50:]
        x = range(1, len(points) + 1)
        
        ax.plot(x, points, 'o-', color='#00b4d8', linewidth=2, markersize=4)
        ax.set_xlabel('Round Number', color='white', fontsize=12)
        ax.set_ylabel('Crash Point (x)', color='white', fontsize=12)
        ax.set_title('📊 Crash Points History', color='white', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.tick_params(colors='white')
        
        self.embed_chart(fig)
    
    def plot_moving_average(self):
        """Plot moving average"""
        self.clear_chart_frame()
        if len(self.history) < 5:
            messagebox.showwarning("Warning", "Add at least 5 points for moving average")
            return
        
        fig, ax = plt.subplots(figsize=(10, 6), facecolor='#1a1a2e')
        ax.set_facecolor('#1a1a2e')
        
        # Implement moving average logic
        ax.text(0.5, 0.5, 'Moving Average Chart\nComing Soon!', 
               horizontalalignment='center', verticalalignment='center',
               transform=ax.transAxes, color='white', fontsize=16)
        ax.set_facecolor('#1a1a2e')
        
        self.embed_chart(fig)
    
    def plot_trend_analysis(self):
        """Plot trend analysis"""
        self.plot_points_chart()  # Temporary implementation
    
    def plot_distribution(self):
        """Plot distribution"""
        self.clear_chart_frame()
        if len(self.history) < 5:
            messagebox.showwarning("Warning", "Add at least 5 points for distribution")
            return
        
        fig, ax = plt.subplots(figsize=(10, 6), facecolor='#1a1a2e')
        ax.set_facecolor('#1a1a2e')
        
        ax.hist(self.history, bins=15, color='#00b4d8', alpha=0.7, edgecolor='white')
        ax.set_xlabel('Crash Point (x)', color='white', fontsize=12)
        ax.set_ylabel('Frequency', color='white', fontsize=12)
        ax.set_title('📈 Points Distribution', color='white', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.tick_params(colors='white')
        
        self.embed_chart(fig)
    
    def plot_profit_trend(self):
        """Plot profit trend"""
        self.clear_chart_frame()
        if len(self.history) < 2:
            messagebox.showwarning("Warning", "Add at least 2 points for profit analysis")
            return
        
        fig, ax = plt.subplots(figsize=(10, 6), facecolor='#1a1a2e')
        ax.set_facecolor('#1a1a2e')
        
        # Calculate cumulative profit
        profits = []
        cumulative = 0
        for point in self.history:
            profit = (point - 1) * 10 if point > 1 else -10
            cumulative += profit
            profits.append(cumulative)
        
        x = range(1, len(profits) + 1)
        ax.plot(x, profits, 'o-', color='#27AE60', linewidth=2)
        ax.set_xlabel('Round Number', color='white', fontsize=12)
        ax.set_ylabel('Cumulative Profit', color='white', fontsize=12)
        ax.set_title('💰 Cumulative Profit Trend', color='white', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.tick_params(colors='white')
        
        self.embed_chart(fig)
    
    def plot_risk_analysis(self):
        """Plot risk analysis"""
        self.plot_distribution()  # Temporary implementation
    
    def clear_chart_frame(self):
        """Clear chart frame"""
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
    
    def embed_chart(self, fig):
        """Embed chart in interface"""
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def bulk_input(self):
        """Bulk input data"""
        messagebox.showinfo("Bulk Input", "Bulk input feature coming soon!")
    
    def clear_history(self):
        """Clear history"""
        if messagebox.askyesno("Confirm", "Clear all data?"):
            self.history.clear()
            self.session_profit = 0
            self.save_data()
            self.update_dashboard()
            messagebox.showinfo("Success", "All data cleared")
    
    def clear_all_data(self):
        """Clear all data"""
        self.clear_history()
    
    def export_data(self):
        """Export data"""
        self.save_data()
        messagebox.showinfo("Export", f"Exported {len(self.history)} points")
    
    def import_data(self):
        """Import data"""
        messagebox.showinfo("Import", "Import feature coming soon!")
    
    def load_data(self):
        """Load saved data"""
        try:
            if os.path.exists('crash_data.json'):
                with open('crash_data.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.history = data.get('history', [])
                    self.session_profit = data.get('profit', 0)
        except:
            self.history = []
    
    def save_data(self):
        """Save data"""
        try:
            data = {
                'history': self.history,
                'profit': self.session_profit,
                'last_update': datetime.now().isoformat()
            }
            with open('crash_data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")
    
    def auto_update(self):
        """Auto-update system"""
        def update():
            while True:
                if self.auto_update_var.get():
                    self.update_dashboard()
                time.sleep(5)  # Update every 5 seconds
        
        thread = threading.Thread(target=update, daemon=True)
        thread.start()

def main():
    root = tk.Tk()
    app = ElegantCrashAnalyzer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
