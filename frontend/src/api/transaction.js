import api from './index';

export const createTransaction = async (data) => {
  const response = await api.post('/transactions', data);
  return response.data;
};

export const getTransactions = async (accountId = null) => {
  const params = accountId ? { account_id: accountId } : {};
  const response = await api.get('/transactions', { params });
  return response.data;
};

export const getTransaction = async (id) => {
  const response = await api.get(`/transactions/${id}`);
  return response.data;
};

export const updateTransaction = async (id, data) => {
  const response = await api.put(`/transactions/${id}`, data);
  return response.data;
};

export const deleteTransaction = async (id) => {
  await api.delete(`/transactions/${id}`);
};