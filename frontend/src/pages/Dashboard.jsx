import { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { createAccount, getAccounts, deleteAccount } from '../api/account';
import { createTransaction, getTransactions, deleteTransaction } from '../api/transaction';
import { createBudget, getBudgets, deleteBudget } from '../api/budget';
import '../App.css';

function Dashboard() {
  const { user } = useContext(AuthContext);
  const [accounts, setAccounts] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [budgets, setBudgets] = useState([]);
  const [accountForm, setAccountForm] = useState({ name: '', account_type: 'savings' });
  const [transactionForm, setTransactionForm] = useState({
    account_id: '',
    amount: '',
    category: '',
    date: new Date().toISOString().slice(0, 16),
    type: 'expense',
    status: 'pending',
    note: '',
  });
  const [budgetForm, setBudgetForm] = useState({ category: '', limit: '', period: '1 month' });
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const accountsData = await getAccounts();
        setAccounts(accountsData);
        const transactionsData = await getTransactions();
        setTransactions(transactionsData);
        const budgetsData = await getBudgets();
        setBudgets(budgetsData);
      } catch (err) {
        setError(err.response?.data?.error || 'Failed to fetch data');
      }
    };
    fetchData();
  }, []);

  const handleAccountSubmit = async (e) => {
    e.preventDefault();
    try {
      const newAccount = await createAccount(accountForm);
      setAccounts([...accounts, newAccount]);
      setAccountForm({ name: '', account_type: 'savings' });
      setError('');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create account');
    }
  };

  const handleTransactionSubmit = async (e) => {
    e.preventDefault();
    try {
      const newTransaction = await createTransaction(transactionForm);
      setTransactions([...transactions, newTransaction]);
      setTransactionForm({ account_id: '', amount: '', category: '', date: new Date().toISOString().slice(0, 16), type: 'expense', status: 'pending', note: '' });
      setError('');
      // Refresh accounts to update balances
      const accountsData = await getAccounts();
      setAccounts(accountsData);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create transaction');
    }
  };

  const handleBudgetSubmit = async (e) => {
    e.preventDefault();
    try {
      const newBudget = await createBudget(budgetForm);
      setBudgets([...budgets, newBudget]);
      setBudgetForm({ category: '', limit: '', period: '1 month' });
      setError('');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create budget');
    }
  };

  const handleDeleteAccount = async (id) => {
    try {
      await deleteAccount(id);
      setAccounts(accounts.filter((account) => account.id !== id));
      setError('');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to delete account');
    }
  };

  const handleDeleteTransaction = async (id) => {
    try {
      await deleteTransaction(id);
      setTransactions(transactions.filter((t) => t.id !== id));
      setError('');
      // Refresh accounts to update balances
      const accountsData = await getAccounts();
      setAccounts(accountsData);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to delete transaction');
    }
  };

  const handleDeleteBudget = async (id) => {
    try {
      await deleteBudget(id);
      setBudgets(budgets.filter((b) => b.id !== id));
      setError('');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to delete budget');
    }
  };

  return (
    <div className="main-content">
      <h1>Dashboard</h1>
      {error && <p className="error">{error}</p>}

      <div className="card">
        <h2>Accounts</h2>
        <form onSubmit={handleAccountSubmit} className="form-container">
          <input
            type="text"
            className="form-input"
            placeholder="Account Name"
            value={accountForm.name}
            onChange={(e) => setAccountForm({ ...accountForm, name: e.target.value })}
          />
          <select
            className="form-input"
            value={accountForm.account_type}
            onChange={(e) => setAccountForm({ ...accountForm, account_type: e.target.value })}
          >
            <option value="savings">Savings</option>
            <option value="checking">Checking</option>
            <option value="cash">Cash</option>
            <option value="investment">Investment</option>
          </select>
          <button type="submit" className="form-button">Add Account</button>
        </form>
        <ul>
          {accounts.map((account) => (
            <li key={account.id}>
              {account.name} ({account.account_type}) - {user.currency} {account.balance.toFixed(2)}
              <button onClick={() => handleDeleteAccount(account.id)} className="form-button">Delete</button>
            </li>
          ))}
        </ul>
      </div>

      <div className="card">
        <h2>Transactions</h2>
        <form onSubmit={handleTransactionSubmit} className="form-container">
          <select
            className="form-input"
            value={transactionForm.account_id}
            onChange={(e) => setTransactionForm({ ...transactionForm, account_id: e.target.value })}
          >
            <option value="">Select Account</option>
            {accounts.map((account) => (
              <option key={account.id} value={account.id}>{account.name}</option>
            ))}
          </select>
          <input
            type="number"
            className="form-input"
            placeholder="Amount"
            value={transactionForm.amount}
            onChange={(e) => setTransactionForm({ ...transactionForm, amount: e.target.value })}
          />
          <input
            type="text"
            className="form-input"
            placeholder="Category"
            value={transactionForm.category}
            onChange={(e) => setTransactionForm({ ...transactionForm, category: e.target.value })}
          />
          <input
            type="datetime-local"
            className="form-input"
            value={transactionForm.date}
            onChange={(e) => setTransactionForm({ ...transactionForm, date: e.target.value })}
          />
          <select
            className="form-input"
            value={transactionForm.type}
            onChange={(e) => setTransactionForm({ ...transactionForm, type: e.target.value })}
          >
            <option value="income">Income</option>
            <option value="expense">Expense</option>
          </select>
          <select
            className="form-input"
            value={transactionForm.status}
            onChange={(e) => setTransactionForm({ ...transactionForm, status: e.target.value })}
          >
            <option value="pending">Pending</option>
            <option value="completed">Completed</option>
            <option value="canceled">Canceled</option>
          </select>
          <input
            type="text"
            className="form-input"
            placeholder="Note (optional)"
            value={transactionForm.note}
            onChange={(e) => setTransactionForm({ ...transactionForm, note: e.target.value })}
          />
          <button type="submit" className="form-button">Add Transaction</button>
        </form>
        <ul>
          {transactions.map((t) => (
            <li key={t.id}>
              {t.category} ({t.type}) - {user.currency} {t.amount.toFixed(2)} on {new Date(t.date).toLocaleString()} ({t.status})
              <button onClick={() => handleDeleteTransaction(t.id)} className="form-button">Delete</button>
            </li>
          ))}
        </ul>
      </div>

      <div className="card">
        <h2>Budgets</h2>
        <form onSubmit={handleBudgetSubmit} className="form-container">
          <input
            type="text"
            className="form-input"
            placeholder="Category"
            value={budgetForm.category}
            onChange={(e) => setBudgetForm({ ...budgetForm, category: e.target.value })}
          />
          <input
            type="number"
            className="form-input"
            placeholder="Limit"
            value={budgetForm.limit}
            onChange={(e) => setBudgetForm({ ...budgetForm, limit: e.target.value })}
          />
          <select
            className="form-input"
            value={budgetForm.period}
            onChange={(e) => setBudgetForm({ ...budgetForm, period: e.target.value })}
          >
            <option value="1 day">1 Day</option>
            <option value="2 days">2 Days</option>
            <option value="1 week">1 Week</option>
            <option value="1 month">1 Month</option>
            <option value="3 months">3 Months</option>
            <option value="6 months">6 Months</option>
            <option value="1 year">1 Year</option>
          </select>
          <button type="submit" className="form-button">Add Budget</button>
        </form>
        <ul>
          {budgets.map((b) => (
            <li key={b.id}>
              {b.category} - {user.currency} {b.limit.toFixed(2)} ({b.period})
              <button onClick={() => handleDeleteBudget(b.id)} className="form-button">Delete</button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default Dashboard;