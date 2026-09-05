function Footer() {
  const links = [
    { label: 'GitHub', href: 'https://github.com/Mustafa-Hazard' },
    { label: 'LinkedIn', href: 'https://www.linkedin.com/in/mustafa642/' },
    { label: 'Portfolio', href: 'https://mustafa-cyberhub.vercel.app/' },
  ]

  return (
    <footer className="border-t border-[#8A8578]/30 mt-12">
      <div className="max-w-[1150px] mx-auto px-6 py-6 flex items-center justify-between">
        <span className="font-mono text-xs text-[#8A8578]">
          Built by Mustafa Muhammad
        </span>
        <div className="flex gap-5">
          {links.map((link) => {
            return (
              <a
                key={link.label}
                href={link.href}
                target="_blank"
                rel="noopener noreferrer"
                className="font-mono text-xs uppercase tracking-wider text-[#8A8578] hover:text-[#EDEAE2] transition-colors"
              >
                {link.label}
              </a>
            )
          })}
        </div>
      </div>
    </footer>
  )
}

export default Footer
