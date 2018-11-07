'use strict'

// Extension button
chrome.browserAction.onClicked.addListener((tab) => {
  console.log('Clicked!')
  let search = {
    title: '* - matthew.fallshaw@gmail.com - Gmail',
    url: 'https://mail.google.com/*'
    // not_url: 'mail'
  }
  focusTab(search)
})

// Private
function assert (condition, message) {
  if (!condition) {
    message = message || 'Assertion failed'
    throw new Error(message)
  }
}

function focusTab (tab) {
  chrome.tabs.get(tab.id, (tabInfo) => {
    chrome.windows.update(tabInfo.windowId, { focused: true }, () => {
      chrome.tabs.update(tab.id, { active: true, highlighted: true })
    })
  })
};

function focusWindowContainingTab (tab) {
  chrome.tabs.get(tab.id, (tabInfo) => {
    chrome.windows.update(tabInfo.windowId, { focused: true })
  })
};

function findTab (search, callback) {
  assert(search.title || search.url || search.not_title || search.not_url,
    'in findAndFocusTab, when passing a table of search parameters, I need one of `title` or `url`')

  // Defaults
  let query = {}
  search.windowType = search.windowType || 'normal';

  ['title', 'url'].forEach((key) => search[key] && (query[key] = search[key]))

  try {
    chrome.tabs.query(query, (tabs) => {
      let found = tabs.some((tab) => {
        if ((!search.not_title || !tab.title.match(new RegExp(search.not_title))) &&
             (!search.not_url || !tab.url.match(new RegExp(search.not_url)))) {
          callback(tab)
          return true
        } else {
          return false
        }
      })
      if (found) {
        return found
      } else {
        console.log('Nothing found.')
        return false
      }
    })
  } catch (err) {
    console.log(err)
  }
};

// Public
function findAndFocusTab (search) {
  findTab(search, focusTab)
}

function findAndFocusWindowContainingTab (search) {
  findTab(search, focusWindowContainingTab)
}

// Listeners
let port = chrome.runtime.connectNative('com.matthewfallshaw.chrometabsfinder')
port.onMessage.addListener((msg) => {
  try {
    let command = msg['msg']
    if (command['focus']) {
      findAndFocusTab(command['focus'])
    } else if (command['focusWindowContaining']) {
      findAndFocusWindowContainingTab(command['focusWindowContaining'])
    }
  } catch (err) {
    console.log(err)
    try {
      console.log('Received poorly formed: ' + JSON.stringify(msg))
    } catch (err) {
      console.log(err)
      console.log('Received very poorly formed: ' + msg)
    }
  }
})
port.onDisconnect.addListener(() => {
  console.log('Disconnected')
})

/* eslint-env webextensions */
