# My-Home-Assistant-Config
This is my personal Home Assistant config including dashboard, automations etc

## Integrations
* Browser mod
* Generic Camera
* Glances
* Google Cast
* HACS
* HomeKit
* IKEA TRÅDFRI
* IPP
* Localtuya
* motionEye
* Node-RED
* OctoPrint
* ONVIF
* OpenWeatherMap
* Powercalc
* Samsung TV
* Shelly
* Sonoff
* Tapo
* Tibber
* Yale

## HACS Frontend
* Weather card
* bignumber-card
* Number box
* mini-graph-card
* Vertical Stack In Card
* Mushroom
* apexcharts-card
* card-mod
* iOS Dark Mode Theme
* Lovelace Wallpanel Screensaver

## Dashboard/Lovelace
I use a wall mounted iPad as a dashboard in kiosk mode. My kiosk works by having fullscreen in HA companion app and using Lovelace Wallpanel Screensaver from HACS that includes both a kiosk mode and a screen saver.

### Home:
<img src="https://github.com/WattageGuy/My-Home-Assistant-Config/blob/main/images/home.png" width="600">
<img src="https://github.com/WattageGuy/My-Home-Assistant-Config/blob/main/images/home-down.png" width="600">

### Lamps:
<img src="https://github.com/WattageGuy/My-Home-Assistant-Config/blob/main/images/lamps.png" width="600">

### Energi:
<img src="https://github.com/WattageGuy/My-Home-Assistant-Config/blob/main/images/energi.png" width="600">
<img src="https://github.com/WattageGuy/My-Home-Assistant-Config/blob/main/images/energi-down.png" width="600">

### Media:
<img src="https://github.com/WattageGuy/My-Home-Assistant-Config/blob/main/images/media.png" width="600">

### Sensors:
<img src="https://github.com/WattageGuy/My-Home-Assistant-Config/blob/main/images/sensors.png" width="600">

### CCTV:
<img src="https://github.com/WattageGuy/My-Home-Assistant-Config/blob/main/images/cctv.png" width="600">

### Kökstimer - Kitchen timer
On dashboard home a kitchen timer can bee seen. This is how its made:

You need:
* Input number helper: input_number.kokstimer_tid_minuter
* Input boolean helper: input_boolean.kokstimer_ljud
* Timer helper: timer.kokstimer
* Script
* Automation
* numberbox-card
* Browser mod
* MP3 Audio

**Card:**
```
type: entities
entities:
  - entity: input_number.kokstimer_tid_minuter
    type: custom:numberbox-card
    icon: mdi:timer-settings
    name: Timer tid i minuter
    delay: 0
    card_mod:
      style: |
        ha-card {
          background: none;
        }
  - entity: script.satt_tid_kokstimer
    icon: mdi:timer-play
    name: Starta timer
  - entity: timer.kokstimer
    name: ' '
    icon: 'null'
    secondary_info: none
  - entity: input_boolean.kokstimer_ljud
    icon: mdi:timer-music
title: Kökstimer
state_color: true
card_mod:
  style: |
    ha-card {
      padding-bottom: 110px;
    }
    hui-timer-entity-row {
      font-size: 50px;
      position: absolute;
      top: 70px;
      line-height: 100%;
      margin-left: -10px;
    }
```

**Script:**
````
alias: Sätt tid kökstimer
sequence:
  - service: timer.start
    data:
      duration: >-
        {{ ((states('input_number.kokstimer_tid_minuter') | float * 60)) |
        round(2) }}
    target:
      entity_id: timer.kokstimer
  - service: input_boolean.turn_on
    data: {}
    target:
      entity_id: input_boolean.kokstimer_ljud
mode: single
````

**Automation:**
````
alias: Kökstimer spela ljud
description: ""
trigger:
  - platform: event
    event_type: timer.finished
    event_data:
      entity_id: timer.kokstimer
condition: []
action:
  - repeat:
      while:
        - condition: state
          entity_id: input_boolean.kokstimer_ljud
          state: "on"
      sequence:
        - delay:
            hours: 0
            minutes: 0
            seconds: 1
            milliseconds: 2
        - service: media_player.play_media
          target:
            entity_id: media_player.ipad_hemkontroll
          data:
            media_content_id: >-
              media-source://media_source/local/synth-twinkle-alert-sound-001-8436.mp3
            media_content_type: audio/mpeg
          metadata:
            title: synth-twinkle-alert-sound-001-8436.mp3
            thumbnail: null
            media_class: music
            children_media_class: null
            navigateIds:
              - {}
              - media_content_type: app
                media_content_id: media-source://media_source
mode: single
