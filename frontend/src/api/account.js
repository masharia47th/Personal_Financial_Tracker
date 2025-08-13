import api from './index';

export const createAccount = async (data) => {
  const response = await api.post('/accounts', data);
  return response.data;
};

export const getAccounts = async () => {
  const response = await api.get('/accounts');
  return response.data;
};

export const getAccount = async (id) => {
  const response = await api.get(`/accounts/${id}`);
  return response.data;
};

export const updateAccount = async (id, data) => {
  const response = await api.put(`/accounts/${id}`, data);
  return response.data;
};

export const deleteAccount = async (id) => {
  await api.delete(`/accounts/${id}`);
};