import { NavLink } from 'react-router-dom'

const navItems = [
  { to: '/', label: 'Overview', end: true },
  { to: '/threats', label: 'Threats', end: false },
  { to: '/trends', label: 'Trends', end: false },
]

function Header() {
  return (
    <header className="border-b border-[#8A8578]/30">
      <div className="max-w-[1150px] mx-auto px-6 py-5 flex items-baseline justify-between">
        <h1 className="font-condensed text-2xl tracking-tight text-[#EDEAE2]">
          Threat Intelligence Dashboard
        </h1>
        <nav className="flex gap-6">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) =>
                `font-mono text-xs uppercase tracking-wider pb-1 border-b-2 transition-colors ${
                  isActive
                    ? 'text-[#EDEAE2] border-[#C97B4A]'
                    : 'text-[#8A8578] border-transparent hover:text-[#EDEAE2]'
                }`
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
      </div>
    </header>
  )
}

export default Header
