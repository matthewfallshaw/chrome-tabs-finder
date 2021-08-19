'use strict'

// Reports status, sets timeout to clear
function reportStatus (message) {
  // Update status to let user know options were saved.
  const status = document.getElementById('status');
  status.textContent = message;
  setTimeout(function () { status.textContent = '' }, 3000);
}

// Saves options to chrome.storage
function saveOptions () {
  const selectedProfile = document.getElementById('profile').value
  chrome.storage.sync.set({ profile: selectedProfile }, function () {
    reportStatus('Options saved.');
  });
}

// Restores select box and checkbox state using the preferences
// stored in chrome.storage.
function restoreOptions () {
  // Use default value profile = 'default'.
  chrome.storage.sync.get('profile', function (items) {
    document.getElementById('profile').value = items.profile;
  });
}

document.addEventListener('DOMContentLoaded', restoreOptions);
document.getElementById('profile').addEventListener('change', saveOptions);

/* eslint-env webextensions */
