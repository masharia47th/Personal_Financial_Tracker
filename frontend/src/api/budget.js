import api from './index';

export const createBudget = async (data) => {
  const response = await api.post('/budgets', data);
  return response.data;
};

export const getBudgets = async () => {
  const response = await api.get('/budgets');
  return response.data;
};

export const getBudget = async (id) => {
  const response = await api.get(`/budgets/${id}`);
  return response.data;
};

export const updateBudget = async (id, data) => {
  const response = await api.put(`/budgets/${id}`, data);
  return response.data;
};

export const deleteBudget = async (id) => {
  await api.delete(`/budgets/${id}`);
};