function Header() {
  return (
    <header className="border-b border-[#8A8578]/30">
      <div className="max-w-[1150px] mx-auto px-6 py-5 flex items-baseline justify-between">
        <h1 className="font-condensed text-2xl tracking-tight text-[#EDEAE2]">
          SupplyChainIQ
        </h1>
        <span className="font-mono text-xs text-[#8A8578]">
          last sync · 2 min ago
        </span>
      </div>
    </header>
  )
}

export default Header
