'use strict'

const NATIVE_HOST = 'com.matthewfallshaw.chrometabsfinder'

// Private
function assert (condition, message) {
  if (!condition) {
    message = message || 'Assertion failed'
    throw new Error(message)
  }
}

function reply (reply, port, profile) {
  const replyText = JSON.stringify({ reply: reply, profile: profile })
  console.log(replyText)
  port.postMessage(replyText)
}

function focusTab (tab, port, profile) {
  chrome.tabs.get(tab.id, (tabInfo) => {
    chrome.windows.update(tabInfo.windowId, { focused: true }, () => {
      chrome.tabs.update(tab.id, { active: true, highlighted: true })
    })
  })
  reply('Focused tab', port, profile)
};

function focusWindowContainingTab (tab, port, profile) {
  chrome.tabs.get(tab.id, (tabInfo) => {
    chrome.windows.update(tabInfo.windowId, { focused: true })
  })
  reply('Focused window', port, profile)
};

function findTab (search, callback, port) {
  assert(search.title || search.url || search.not_title || search.not_url,
    'in findAndFocusTab, when passing a table of search parameters, I need one of `title` or `url`')

  // Check for unexpected search properties
  Object.keys(search).forEach((key) => {
    if (!['title', 'url', 'not_title', 'not_url', 'profile'].includes(key)) {
      console.log('warning: search includes unexpected key ' + key)
    }
  })

  // chrome.tabs.query query object from search object
  const query = {}
  search.windowType = search.windowType || 'normal';
  ['title', 'url'].forEach((key) => search[key] && (query[key] = search[key]))

  function findTabs (search, callback, port, profile) {
    try {
      chrome.tabs.query(query, (tabs) => {
        const found = tabs.some((tab) => {
          if ((!search.not_title || !tab.title.match(new RegExp(search.not_title))) &&
               (!search.not_url || !tab.url.match(new RegExp(search.not_url)))) {
            callback(tab, port, profile)
            return true
          } else {
            return false
          }
        })
        if (!found) {
          reply('findTab: Nothing found.', port, profile)
        }
      })
    } catch (err) {
      console.log(err)
      reply('findTab: Unhandled error.', port, profile)
    }
  }

  // First check profile…
  chrome.storage.sync.get('profile', (items) => {
    const profile = items.profile || 'default'
    if (search.profile && (search.profile !== profile)) {
      // … if profile doesn't match, fail
      reply('findTab: Wrong profile - wanted:' + search.profile + '.', port, profile)
      return false
    } else {
      // … if profile does match, search tabs
      return findTabs(search, callback, port, profile)
    }
  })
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

// Defaults
chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.sync.get('profile', (items) => {
    if (typeof items.profile === 'undefined') {
      chrome.storage.sync.set({ profile: 'default' })
    }
  })
})

// Listeners
function connect () {
  let port = chrome.runtime.connectNative(NATIVE_HOST)
  port.onMessage.addListener((msg) => {
    try {
      const command = msg['msg']
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
