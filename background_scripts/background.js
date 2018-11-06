'use strict'

// Extension button
chrome.browserAction.onClicked.addListener(function (tab) {
  console.log('Clicked!')
  let search = {
    title: '* - matthew.fallshaw@gmail.com - Gmail',
    url: 'https://mail.google.com/*'
    // not_url: 'mail'
  }
  findTab(search)
})

// Private
function assert (condition, message) {
  if (!condition) {
    message = message || 'Assertion failed'
    throw new Error(message)
  }
}

function focusTab (tab) {
  chrome.tabs.get(tab.id, function (tabInfo) {
    chrome.windows.update(tabInfo.windowId, { focused: true }, function () {
      chrome.tabs.update(tab.id, { active: true, highlighted: true })
      console.log('Focused tab: ' + tab.title + ' in window: ' + tabInfo.windowId)
    })
  })
};

// Public
function findTab (search) {
  assert(search.title || search.url || search.not_title || search.not_url,
    'in findTab, when passing a table of search parameters, I need one of `title` or `url`')

  // Defaults
  let query = {}
  search.windowType = search.windowType || 'normal';

  ['title', 'url'].forEach((key) => search[key] && (query[key] = search[key]))

  // DEBUG
  console.log('Search:')
  console.log(search)

  chrome.tabs.query(query, function (tabs) {
    // DEBUG
    console.log('Tabs:')
    console.log(tabs)
    if (tabs.length === 0) { console.log('`tabs` length: 0.') };

    let found = tabs.some((tab) => {
      // DEBUG
      console.log('Candidate tab: ' + tab.title)

      if ((!search.not_title || !tab.title.match(new RegExp(search.not_title))) &&
           (!search.not_url || !tab.url.match(new RegExp(search.not_url)))) {
        focusTab(tab)
        return true
      } else {
        return false
      }
    })
    if (!found) { console.log('Nothing found.') }
  })
};

// Listeners
let port = chrome.runtime.connectNative('com.matthewfallshaw.chrometabsfinder')
port.onMessage.addListener(function (msg) {
  let command = msg['msg']
  console.log('Received ' + JSON.stringify(command))
  if (command['search']) { findTab(command['search']) }
})
port.onDisconnect.addListener(function () {
  console.log('Disconnected')
})

/* eslint-env webextensions */
