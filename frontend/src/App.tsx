import { Routes, Route } from 'react-router-dom'
import Header from './components/Header'
import Footer from './components/Footer'
import Overview from './pages/Overview'
import Threats from './pages/Threats'
import Trends from './pages/Trends'

function App() {
  return (
    <div className="min-h-screen bg-[#12181F] flex flex-col">
      <Header />
      <main className="max-w-[1150px] mx-auto px-6 py-10 flex-1 w-full">
        <Routes>
          <Route path="/" element={<Overview />} />
          <Route path="/threats" element={<Threats />} />
          <Route path="/trends" element={<Trends />} />
        </Routes>
      </main>
      <Footer />
    </div>
  )
}

export default App
