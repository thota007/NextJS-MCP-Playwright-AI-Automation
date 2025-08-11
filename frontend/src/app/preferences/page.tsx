'use client';

import { useState, useEffect } from 'react';
import Layout from '@/components/Layout';
import { apiService, UserData, UserResponse } from '@/lib/api';

export default function PreferencesPage() {
  const [userData, setUserData] = useState<UserData>({
    name: '',
    email: '',
    mhmd_preference: 'OPT_OUT'
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  // Load user data on component mount
  useEffect(() => {
    loadUserData();
  }, []);

  const loadUserData = async () => {
    try {
      const response = await apiService.getUserData();
      if (response.success && response.data) {
        setUserData(response.data);
      }
    } catch (err) {
      console.error('Failed to load user data:', err);
    }
  };

  const handleSave = async () => {
    if (!userData.name || !userData.email) {
      setError('Name and email are required');
      return;
    }

    setLoading(true);
    setError('');
    setMessage('');

    try {
      const response = await apiService.createUserData(userData);
      if (response.success) {
        setMessage('User data saved successfully!');
        setTimeout(() => setMessage(''), 3000);
      } else {
        setError(response.message || 'Failed to save user data');
      }
    } catch (err) {
      setError('Failed to save user data');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete all user data? This action cannot be undone.')) {
      return;
    }

    setLoading(true);
    setError('');
    setMessage('');

    try {
      const response = await apiService.deleteUserData();
      if (response.success) {
        setUserData({
          name: '',
          email: '',
          mhmd_preference: 'OPT_OUT'
        });
        setMessage('User data deleted successfully!');
        setTimeout(() => setMessage(''), 3000);
      } else {
        setError(response.message || 'Failed to delete user data');
      }
    } catch (err) {
      setError('Failed to delete user data');
    } finally {
      setLoading(false);
    }
  };

  const updateField = (field: keyof UserData, value: string) => {
    setUserData(prev => ({ ...prev, [field]: value }));
    setError(''); // Clear error when user starts typing
  };

  return (
    <Layout>
      <div className="max-w-2xl mx-auto px-6">
        <div className="bg-white rounded-lg shadow-md p-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-6">
            User Preferences
          </h1>
          <p className="text-gray-600 mb-8">
            Manage your personal information and My Health My Data (MHMD) preferences.
          </p>

          {/* Messages */}
          {message && (
            <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-md">
              <p className="text-green-800">{message}</p>
            </div>
          )}
          
          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-md">
              <p className="text-red-800">{error}</p>
            </div>
          )}

          <div className="space-y-6">
            {/* Personal Information */}
            <div className="border-b border-gray-200 pb-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                Personal Information
              </h2>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Full Name *
                  </label>
                  <input
                    type="text"
                    value={userData.name}
                    onChange={(e) => updateField('name', e.target.value)}
                    placeholder="Enter your full name"
                    className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-black"
                    disabled={loading}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Email Address *
                  </label>
                  <input
                    type="email"
                    value={userData.email}
                    onChange={(e) => updateField('email', e.target.value)}
                    placeholder="Enter your email address"
                    className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-black"
                    disabled={loading}
                  />
                </div>
              </div>
            </div>

            {/* MHMD Preference */}
            <div className="pb-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                My Health My Data (MHMD) Preference
              </h2>
              <p className="text-sm text-gray-600 mb-4">
                Choose whether you want to opt in or opt out of the My Health My Data program.
              </p>
              
              <div className="space-y-3">
                <div className="flex items-center">
                  <input
                    type="radio"
                    id="opt_in"
                    name="mhmd_preference"
                    value="OPT_IN"
                    checked={userData.mhmd_preference === 'OPT_IN'}
                    onChange={(e) => updateField('mhmd_preference', e.target.value as 'OPT_IN' | 'OPT_OUT')}
                    className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300"
                    disabled={loading}
                  />
                  <label htmlFor="opt_in" className="ml-3 block text-sm text-gray-900">
                    <span className="font-medium text-green-600">OPT IN</span> - I want to participate in the MHMD program
                  </label>
                </div>
                
                <div className="flex items-center">
                  <input
                    type="radio"
                    id="opt_out"
                    name="mhmd_preference"
                    value="OPT_OUT"
                    checked={userData.mhmd_preference === 'OPT_OUT'}
                    onChange={(e) => updateField('mhmd_preference', e.target.value as 'OPT_IN' | 'OPT_OUT')}
                    className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300"
                    disabled={loading}
                  />
                  <label htmlFor="opt_out" className="ml-3 block text-sm text-gray-900">
                    <span className="font-medium text-red-600">OPT OUT</span> - I do not want to participate in the MHMD program
                  </label>
                </div>
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex space-x-4 pt-6 border-t border-gray-200">
            <button
              onClick={handleSave}
              disabled={loading || !userData.name || !userData.email}
              className="bg-indigo-600 text-white px-6 py-3 rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Saving...' : 'Save Preferences'}
            </button>
            
            <button
              onClick={handleDelete}
              disabled={loading}
              className="bg-red-600 text-white px-6 py-3 rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Delete Data
            </button>
          </div>

          {/* Current Data Summary */}
          {(userData.name || userData.email) && (
            <div className="mt-8 p-4 bg-gray-50 rounded-lg">
              <h3 className="text-sm font-medium text-gray-900 mb-2">Current Data Summary</h3>
              <div className="text-sm text-gray-600 space-y-1">
                <div>Name: <span className="font-medium">{userData.name || 'Not set'}</span></div>
                <div>Email: <span className="font-medium">{userData.email || 'Not set'}</span></div>
                <div>MHMD Preference: <span className={`font-medium ${
                  userData.mhmd_preference === 'OPT_IN' ? 'text-green-600' : 'text-red-600'
                }`}>{userData.mhmd_preference}</span></div>
              </div>
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}