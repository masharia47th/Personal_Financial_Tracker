import { useContext } from 'react'
import { AuthContext } from '../context/AuthContext'
import '../App.css'

function Dashboard() {
  const { user } = useContext(AuthContext)

  return (
    <div className="card">
      <h2>Welcome, {user.username}!</h2>
      <p>Your preferred currency: {user.currency}</p>
      <p>This is your personal finance dashboard. More features coming soon!</p>
    </div>
  )
}

export default Dashboard