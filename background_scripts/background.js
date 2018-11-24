'use strict'

const NATIVE_HOST = 'com.matthewfallshaw.chrometabsfinder'

// Private
function assert (condition, message) {
  if (!condition) {
    message = message || 'Assertion failed'
    throw new Error(message)
  }
}

function reply (reply, port) {
  console.log(JSON.stringify(reply))
  port.postMessage({ reply: reply })
}

function focusTab (tab, port) {
  chrome.tabs.get(tab.id, (tabInfo) => {
    chrome.windows.update(tabInfo.windowId, { focused: true }, () => {
      chrome.tabs.update(tab.id, { active: true, highlighted: true })
    })
  })
  reply('Focused tab', port)
};

function focusWindowContainingTab (tab, port) {
  chrome.tabs.get(tab.id, (tabInfo) => {
    chrome.windows.update(tabInfo.windowId, { focused: true })
  })
  reply('Focused window', port)
};

function findTab (search, callback, port) {
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
          callback(tab, port)
          return true
        } else {
          return false
        }
      })
      if (!found) {
        reply('findTab: Nothing found.', port)
      }
    })
  } catch (err) {
    console.log(err)
    reply('Unhandled error.', port)
  }
};

// Public
function findAndFocusTab (search, port) {
  findTab(search, focusTab, port)
}

function findAndFocusWindowContainingTab (search, port) {
  findTab(search, focusWindowContainingTab, port)
}

function getAllTabs (port) {
  chrome.windows.getAll({ populate: true }, (windows) => {
    reply({ windows: windows.reduce((all, one) => { return all.concat(one.tabs) }, []) }, port)
  })
}

// Listeners
function connect () {
  let port = chrome.runtime.connectNative(NATIVE_HOST)
  port.onMessage.addListener((msg) => {
    try {
      let command = msg['msg']
      if (command['focus']) {
        console.log('Focusing a tab')
        findAndFocusTab(command['focus'], port)
      } else if (command['focusWindowContaining']) {
        console.log('Focusing a window')
        findAndFocusWindowContainingTab(command['focusWindowContaining'], port)
      } else if (command === 'getAllTabs') {
        console.log('getAllTabs')
        getAllTabs(port)
      } else {
        reply('Unrecognised command: ' + JSON.stringify(command), port)
      }
    } catch (err) {
      console.log(err)
      try {
        reply('Received poorly formed: ' + JSON.stringify(msg), port)
      } catch (err) {
        console.log(err)
        reply('Received very poorly formed: ' + msg, port)
      }
    }
  })
  port.onDisconnect.addListener(() => {
    console.log('Disconnected, reconnecting')
    port = connect()
  })
  return port
}
connect()

/* eslint-env webextensions */
