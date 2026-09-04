import Header from './components/Header'
import SummaryPanel from './components/SummaryPanel'
import ThreatTable from './components/ThreatTable'
import TrendChart from './components/TrendChart'

function App() {
  return (
    <div className="min-h-screen bg-[#12181F]">
      <Header />
      <main className="max-w-[1150px] mx-auto px-6 py-10 space-y-8">
        <SummaryPanel />
        <ThreatTable />
        <TrendChart />
      </main>
    </div>
  )
}

export default App
