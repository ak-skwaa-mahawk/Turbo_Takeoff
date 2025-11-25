{suppliers.map((supplier) => (
  <div key={supplier.name} className="bg-slate-700/30 rounded-lg p-4 flex items-center justify-between">
    <div className="flex items-center gap-4">
      <span className="text-sm text-slate-400">#{supplier.priority}</span>
      <span className="font-semibold">{supplier.name}</span>
    </div>
    <div className="flex items-center gap-4">
      <div className="w-32 bg-slate-600 rounded-full h-2">
        <div 
          className={`h-2 rounded-full ${
            supplier.resonance >= 80 ? 'bg-green-500' : 
            supplier.resonance >= 60 ? 'bg-yellow-500' : 'bg-red-500'
          }`}
          style={{ width: `${supplier.resonance}%` }}
        ></div>
      </div>
      <span className="text-sm font-semibold w-12">{supplier.resonance}/100</span>
    </div>
  </div>
))}