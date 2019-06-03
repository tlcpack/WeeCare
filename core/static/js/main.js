
const changeNotificationUrl = '/home/change_notification/'
const feedNotificationUrl = '/home/feed_notification/'
const napNotificationUrl = '/home/nap_notification/'

function getChangeNotification (changeNotificationUrl) {
  let promise = fetch(changeNotificationUrl).then(function (response) {
    if (!response.ok) {
      throw Error(response.statusText)
    }
    return response.json()
  })
  return promise
}

function getChangeNotificationData (changeNotificationUrl) {
  getChangeNotification(changeNotificationUrl)
    .then(notificationData => {
      for (let notification of Object.values(notificationData)) {
        for (let child of notification) {
          if (document.getElementById(`${child}`)) {
            childDiv = document.getElementById(`${child}`)
            childDiv.classList.add('show')
          }
        }
      }
    })
}

function getFeedNotification (feedNotificationUrl) {
  let promise = fetch(feedNotificationUrl).then(function (response) {
    if (!response.ok) {
      throw Error(response.statusText)
    }
    return response.json()
  })
  return promise
}

function getFeedNotificationData (feedNotificationUrl) {
  getFeedNotification(feedNotificationUrl)
    .then(feedNotificationData => {
      for (let notification of Object.values(feedNotificationData)) {
        for (let child of notification) {
          if (document.getElementById(`feed_${child}`)) {
            feedChildDiv = document.getElementById(`feed_${child}`)
            feedChildDiv.classList.add('show')
          }
        }
      }
    })
}

function getNapNotification (napNotificationUrl) {
  let promise = fetch(napNotificationUrl).then(function (response) {
    if (!response.ok) {
      throw Error(response.statusText)
    }
    return response.json()
  })
  return promise
}

function getNapNotificationData (napNotificationUrl) {
  getNapNotification(napNotificationUrl)
    .then(napNotificationData => {
      for (let notification of Object.values(napNotificationData)) {
        for (let child of notification) {
          if (document.getElementById(`nap_${child}`)) {
            napChildDiv = document.getElementById(`nap_${child}`)
            napChildDiv.classList.add('show')
          }
        }
      }
    })
}

function validateBottleForm () {
  const radios = document.getElementsByName('bottle_choice')
  let formValid = false

  let i = 0
  while (!formValid && i < radios.length) {
    if (radios[i].checked) formValid = true
    i++
  }
  if (!formValid) alert('Must choose a bottle option!')
  return formValid
}

function submitBottleForm () {
  if (validateBottleForm()) document.getElementById('bottle_form').submit()
}

function validateNurseForm () {
  const radios = document.getElementsByName('nurse_choice')
  let formValid = false

  let i = 0
  while (!formValid && i < radios.length) {
    if (radios[i].checked) formValid = true
    i++
  }
  if (!formValid) alert('Must choose a nurse option!')
  return formValid
}

function submitNurseForm () {
  if (validateNurseForm()) document.getElementById('nurse_form').submit()
}

function validateFoodForm () {
  const radios = document.getElementsByName('food_choice')
  let formValid = false

  let i = 0
  while (!formValid && i < radios.length) {
    if (radios[i].checked) formValid = true
    i++
  }
  if (!formValid) alert('Must choose a food option!')
  return formValid
}

function submitFoodForm () {
  if (validateFoodForm()) document.getElementById('food_form').submit()
}

function myBottleFunction () {
  document.getElementById('bottleChoices').classList.toggle('show')
}

function myNurseFunction () {
  document.getElementById('nurseChoices').classList.toggle('show')
}

function myLunchFunction () {
  document.getElementById('lunchChoices').classList.toggle('show')
}

function myDiaperFunction () {
  document.getElementById('diaperChoices').classList.toggle('show')
}

window.onclick = function (event) {
  if (!event.target.matches('.dropButton')) {
    var dropdowns = document.getElementsByClassName('dropdownContent')
    var i
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i]
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show')
      }
    }
  }
}

document.addEventListener('DOMContentLoaded', function () {
  setInterval(function () {
    getChangeNotificationData(changeNotificationUrl)
  }, 10000)
  setInterval(function () {
    getFeedNotificationData(feedNotificationUrl)
  }, 5000)
  setInterval(function () {
    getNapNotificationData(napNotificationUrl)
  }, 3000)
})
