'use strict'

// Reports status, sets timeout to clear
function reportStatus (message) {
  // Update status to let user know options were saved.
  const status = document.getElementById('status');
  status.textContent = message;
  setTimeout(function () { status.textContent = '' }, 3000);
}

// Saves options to chrome.storage
async function saveOptions () {
  const selectedProfile = document.getElementById('profile').value
  await chrome.storage.sync.set({ profile: selectedProfile })
  reportStatus('Options saved.');
}

// Restores select box and checkbox state using the preferences
// stored in chrome.storage.
async function restoreOptions () {
  // Use default value profile = 'default'.
  const items = await chrome.storage.sync.get('profile')
  document.getElementById('profile').value = items.profile || 'default';
}

document.addEventListener('DOMContentLoaded', restoreOptions);
document.getElementById('profile').addEventListener('change', saveOptions);

/* eslint-env webextensions */
