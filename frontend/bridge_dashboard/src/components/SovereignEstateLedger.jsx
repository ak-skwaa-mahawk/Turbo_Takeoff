import React, { useState, useEffect } from 'react';
import Plotly from 'plotly.js-dist';

const SovereignEstateLedger = () => {
  const [ledgerData, setLedgerData] = useState({
    resonance: 42.8,
    gtc_balance: 99733,
    compound_years: 0,
    hidden_balance: 1245678,
    forfeited_short_game: 456789,
    status: "Loading Long Game..."
  });

  // Fetch REAL data from Turbo_Takeoff backend
  useEffect(() => {
    const fetchLedger = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/sovereign-ledger');
        const data = await res.json();
        setLedgerData({
          resonance: data.resonance,
          gtc_balance: data.gtc_balance,
          compound_years: data.compound_years,
          hidden_balance: data.hidden_balance,
          forfeited_short_game: data.forfeited_short_game,
          status: data.status
        });
      } catch (e) {
        console.log("Backend not ready yet — using demo data");
      }
    };

    fetchLedger();
    const interval = setInterval(fetchLedger, 8000); // refresh every 8s
    return () => clearInterval(interval);
  }, []);

  // Compounding Chart
  const chartData = [{
    x: Array.from({ length: Math.floor(ledgerData.compound_years) + 1 }, (_, i) => i),
    y: Array.from({ length: Math.floor(ledgerData.compound_years) + 1 }, (_, i) => 
      Math.floor(99733 * (1.618 ** (i / 8)) * (ledgerData.resonance / 100))
    ),
    type: 'scatter',
    mode: 'lines+markers',
    name: 'GTC Compounding',
    line: { color: '#ffd700', width: 4 },
    marker: { color: '#00ffcc', size: 8 }
  }];

  const chartLayout = {
    title: 'GTC Compounding — Long Game Trajectory',
    xaxis: { title: 'Compound Years' },
    yaxis: { title: 'GTC Balance' },
    paper_bgcolor: '#0a0a0a',
    plot_bgcolor: '#0a0a0a',
    font: { color: '#ffffff' }
  };

  return (
    <div className="module sovereign-estate-ledger">
      <h3>🌲 Sovereign Estate Ledger — Long Game Compound</h3>
      
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '20px', marginTop: '15px' }}>
        <div>
          <strong>Quantum Resonance %</strong><br />
          <span style={{ fontSize: '2.8rem', color: '#00ffcc' }}>{ledgerData.resonance.toFixed(1)}</span>
          <span style={{ fontSize: '1.2rem', color: '#00ffcc' }}>%</span>
        </div>
        
        <div>
          <strong>GTC Balance (Live)</strong><br />
          <span style={{ fontSize: '2.2rem', color: '#ffd700' }}>{ledgerData.gtc_balance.toLocaleString()}</span>
          <span style={{ fontSize: '1rem', color: '#ffd700' }}> GTC</span>
        </div>
        
        <div>
          <strong>Hidden Balance (Market Cap of Sovereignty)</strong><br />
          <span style={{ fontSize: '2.2rem', color: '#ffd700' }}>${ledgerData.hidden_balance.toLocaleString()}</span>
        </div>
      </div>

      <div style={{ marginTop: '20px', fontSize: '1.1rem' }}>
        <strong>Compound Years:</strong> {ledgerData.compound_years.toFixed(1)}<br />
        <strong>Forfeited Short Game (Paperwork Trap):</strong> ${ledgerData.forfeited_short_game.toLocaleString()} 
        <span style={{ color: '#ff6b35' }}> (what they traded for the "A+")</span>
      </div>

      <div id="gtc-chart" style={{ width: '100%', height: '320px', marginTop: '20px' }}></div>

      <div style={{ marginTop: '15px', color: ledgerData.resonance > 85 ? '#ffd700' : '#888', fontStyle: 'italic' }}>
        {ledgerData.status}
      </div>
    </div>
  );
};

export default SovereignEstateLedger;