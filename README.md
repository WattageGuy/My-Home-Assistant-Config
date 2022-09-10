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

````
## Food Anouncer - Matroparen:
This card lets anyone broadcast a message to devices (made for food announcments):

You need:
* input_select.matroparen_vem
* input_text.matroparen_text
* switch.lovelace_button (Node-RED)
* Node-RED
* Nest (Optional)
* Browser mod (Optional)

**Node-RED:**

<details closed>
<summary>Node-RED Flow JSON</summary>
<br>
Import this into Node-RED:
<br>
[{"id":"afdad340469dd9d3","type":"tab","label":"Flow 2","disabled":false,"info":"","env":[]},{"id":"08c6f5b9d241ef17","type":"ha-entity","z":"afdad340469dd9d3","name":"","server":"7874f07a.dd83f","version":2,"debugenabled":false,"outputs":2,"entityType":"switch","config":[{"property":"name","value":"Lovelace Button"},{"property":"device_class","value":""},{"property":"icon","value":""},{"property":"unit_of_measurement","value":""},{"property":"state_class","value":""},{"property":"last_reset","value":""}],"state":"payload","stateType":"msg","attributes":[],"resend":true,"outputLocation":"","outputLocationType":"none","inputOverride":"allow","outputOnStateChange":false,"outputPayload":"","outputPayloadType":"str","x":110,"y":240,"wires":[["0a19a85f0ac68f61","3c7ad5013e6f8ae7","a8a4397a7ddfedf9"],[]]},{"id":"0a19a85f0ac68f61","type":"function","z":"afdad340469dd9d3","name":"DC Request","func":"var message;\n\nif (global.get(\"homeassistant.homeAssistant.states['input_text.matroparen_text'].state\") == \"\") {\n    message = \"Matdax!\";\n} else {\n    message = global.get(\"homeassistant.homeAssistant.states['input_text.matroparen_text'].state\");\n}\n\nif (global.get(\"homeassistant.homeAssistant.states['input_select.matroparen_vem'].state\") == \"name\" || global.get(\"homeassistant.homeAssistant.states['input_select.matroparen_vem'].state\") == \"Both\") {\n    msg.method = \"POST\";\n    msg.url = \"https://discordapp.com/api/webhooks//\";\n    msg.payload = { \"content\": message };\n    return msg;\n}","outputs":1,"noerr":0,"initialize":"","finalize":"","libs":[],"x":390,"y":200,"wires":[["a00736dcc8b8c48a"]]},{"id":"a00736dcc8b8c48a","type":"http request","z":"afdad340469dd9d3","name":"","method":"use","ret":"txt","paytoqs":"ignore","url":"","tls":"","persist":false,"proxy":"","insecureHTTPParser":false,"authType":"","senderr":false,"headers":[],"credentials":{"user":"","password":""},"x":610,"y":200,"wires":[["0d694ab3c96414a8","f99d32651f8ddfa5"]]},{"id":"3c7ad5013e6f8ae7","type":"function","z":"afdad340469dd9d3","name":"Nest Request","func":"var message;\n\nif (global.get(\"homeassistant.homeAssistant.states['input_text.matroparen_text'].state\") == \"\") {\n    message = \"Matdax!\";\n} else {\n    message = global.get(\"homeassistant.homeAssistant.states['input_text.matroparen_text'].state\");\n}\n\nif (global.get(\"homeassistant.homeAssistant.states['input_select.matroparen_vem'].state\") == \"Name\" || global.get(\"homeassistant.homeAssistant.states['input_select.matroparen_vem'].state\") == \"Båda\") {\n    msg.method = \"POST\";\n    msg.url = \"http://ip:8123/api/webhook/food\";\n    msg.payload = { \"value1\": message };\n    return msg;\n}","outputs":1,"noerr":0,"initialize":"","finalize":"","libs":[],"x":400,"y":240,"wires":[["dd4d7cb39c7d3ef7"]]},{"id":"dd4d7cb39c7d3ef7","type":"http request","z":"afdad340469dd9d3","name":"","method":"use","ret":"txt","paytoqs":"ignore","url":"","tls":"","persist":false,"proxy":"","insecureHTTPParser":false,"authType":"","senderr":false,"headers":[],"x":610,"y":240,"wires":[["0d694ab3c96414a8"]]},{"id":"a8a4397a7ddfedf9","type":"function","z":"afdad340469dd9d3","name":"DC Request 2","func":"var message;\n\nif (global.get(\"homeassistant.homeAssistant.states['input_text.matroparen_text'].state\") == \"\") {\n    message = \"Matdax!\";\n} else {\n    message = global.get(\"homeassistant.homeAssistant.states['input_text.matroparen_text'].state\");\n}\n\nif (global.get(\"homeassistant.homeAssistant.states['input_select.matroparen_vem'].state\") == \"name\" || global.get(\"homeassistant.homeAssistant.states['input_select.matroparen_vem'].state\") == \"Both\") {\n    msg.method = \"POST\";\n    msg.url = \"https://discord.com/api/webhooks//\";\n    msg.payload = {\"content\": message};\n    return msg;\n}","outputs":1,"noerr":0,"initialize":"","finalize":"","libs":[],"x":400,"y":320,"wires":[["6ba40ed11ef5bc26"]]},{"id":"6ba40ed11ef5bc26","type":"http request","z":"afdad340469dd9d3","name":"","method":"use","ret":"txt","paytoqs":"ignore","url":"","tls":"","persist":false,"proxy":"","insecureHTTPParser":false,"authType":"","senderr":false,"headers":[],"x":610,"y":320,"wires":[["0d694ab3c96414a8","f99d32651f8ddfa5"]]},{"id":"0d694ab3c96414a8","type":"debug","z":"afdad340469dd9d3","name":"debug 3","active":true,"tosidebar":true,"console":false,"tostatus":false,"complete":"payload","targetType":"msg","statusVal":"","statusType":"auto","x":880,"y":400,"wires":[]},{"id":"f99d32651f8ddfa5","type":"api-call-service","z":"afdad340469dd9d3","name":"","server":"7874f07a.dd83f","version":5,"debugenabled":false,"domain":"browser_mod","service":"notification","areaId":[],"deviceId":[],"entityId":[],"data":"{\"message\":\"Matroparen skickad!\"}","dataType":"json","mergeContext":"","mustacheAltTags":false,"outputProperties":[],"queue":"first","x":890,"y":240,"wires":[[]]},{"id":"7874f07a.dd83f","type":"server","name":"Home Assistant","version":4,"addon":true,"rejectUnauthorizedCerts":true,"ha_boolean":"y|yes|true|on|home|open","connectionDelay":true,"cacheJson":true,"heartbeat":false,"heartbeatInterval":30,"areaSelector":"friendlyName","deviceSelector":"friendlyName","entitySelector":"friendlyName","statusSeparator":"at: ","statusYear":"hidden","statusMonth":"short","statusDay":"numeric","statusHourCycle":"h23","statusTimeFormat":"h:m"}]
<br><br>
<pre>
&lt;details open&gt;
&lt;summary&gt;Node-RED Flow JSON&lt;&#47;summary&gt;
&lt;br&gt;
Import this into Node-RED:
<br>
[{"id":"afdad340469dd9d3","type":"tab","label":"Flow 2","disabled":false,"info":"","env":[]},{"id":"08c6f5b9d241ef17","type":"ha-entity","z":"afdad340469dd9d3","name":"","server":"7874f07a.dd83f","version":2,"debugenabled":false,"outputs":2,"entityType":"switch","config":[{"property":"name","value":"Lovelace Button"},{"property":"device_class","value":""},{"property":"icon","value":""},{"property":"unit_of_measurement","value":""},{"property":"state_class","value":""},{"property":"last_reset","value":""}],"state":"payload","stateType":"msg","attributes":[],"resend":true,"outputLocation":"","outputLocationType":"none","inputOverride":"allow","outputOnStateChange":false,"outputPayload":"","outputPayloadType":"str","x":110,"y":240,"wires":[["0a19a85f0ac68f61","3c7ad5013e6f8ae7","a8a4397a7ddfedf9"],[]]},{"id":"0a19a85f0ac68f61","type":"function","z":"afdad340469dd9d3","name":"DC Request","func":"var message;\n\nif (global.get(\"homeassistant.homeAssistant.states['input_text.matroparen_text'].state\") == \"\") {\n    message = \"Matdax!\";\n} else {\n    message = global.get(\"homeassistant.homeAssistant.states['input_text.matroparen_text'].state\");\n}\n\nif (global.get(\"homeassistant.homeAssistant.states['input_select.matroparen_vem'].state\") == \"name\" || global.get(\"homeassistant.homeAssistant.states['input_select.matroparen_vem'].state\") == \"Both\") {\n    msg.method = \"POST\";\n    msg.url = \"https://discordapp.com/api/webhooks//\";\n    msg.payload = { \"content\": message };\n    return msg;\n}","outputs":1,"noerr":0,"initialize":"","finalize":"","libs":[],"x":390,"y":200,"wires":[["a00736dcc8b8c48a"]]},{"id":"a00736dcc8b8c48a","type":"http request","z":"afdad340469dd9d3","name":"","method":"use","ret":"txt","paytoqs":"ignore","url":"","tls":"","persist":false,"proxy":"","insecureHTTPParser":false,"authType":"","senderr":false,"headers":[],"credentials":{"user":"","password":""},"x":610,"y":200,"wires":[["0d694ab3c96414a8","f99d32651f8ddfa5"]]},{"id":"3c7ad5013e6f8ae7","type":"function","z":"afdad340469dd9d3","name":"Nest Request","func":"var message;\n\nif (global.get(\"homeassistant.homeAssistant.states['input_text.matroparen_text'].state\") == \"\") {\n    message = \"Matdax!\";\n} else {\n    message = global.get(\"homeassistant.homeAssistant.states['input_text.matroparen_text'].state\");\n}\n\nif (global.get(\"homeassistant.homeAssistant.states['input_select.matroparen_vem'].state\") == \"Name\" || global.get(\"homeassistant.homeAssistant.states['input_select.matroparen_vem'].state\") == \"Båda\") {\n    msg.method = \"POST\";\n    msg.url = \"http://ip:8123/api/webhook/food\";\n    msg.payload = { \"value1\": message };\n    return msg;\n}","outputs":1,"noerr":0,"initialize":"","finalize":"","libs":[],"x":400,"y":240,"wires":[["dd4d7cb39c7d3ef7"]]},{"id":"dd4d7cb39c7d3ef7","type":"http request","z":"afdad340469dd9d3","name":"","method":"use","ret":"txt","paytoqs":"ignore","url":"","tls":"","persist":false,"proxy":"","insecureHTTPParser":false,"authType":"","senderr":false,"headers":[],"x":610,"y":240,"wires":[["0d694ab3c96414a8"]]},{"id":"a8a4397a7ddfedf9","type":"function","z":"afdad340469dd9d3","name":"DC Request 2","func":"var message;\n\nif (global.get(\"homeassistant.homeAssistant.states['input_text.matroparen_text'].state\") == \"\") {\n    message = \"Matdax!\";\n} else {\n    message = global.get(\"homeassistant.homeAssistant.states['input_text.matroparen_text'].state\");\n}\n\nif (global.get(\"homeassistant.homeAssistant.states['input_select.matroparen_vem'].state\") == \"name\" || global.get(\"homeassistant.homeAssistant.states['input_select.matroparen_vem'].state\") == \"Both\") {\n    msg.method = \"POST\";\n    msg.url = \"https://discord.com/api/webhooks//\";\n    msg.payload = {\"content\": message};\n    return msg;\n}","outputs":1,"noerr":0,"initialize":"","finalize":"","libs":[],"x":400,"y":320,"wires":[["6ba40ed11ef5bc26"]]},{"id":"6ba40ed11ef5bc26","type":"http request","z":"afdad340469dd9d3","name":"","method":"use","ret":"txt","paytoqs":"ignore","url":"","tls":"","persist":false,"proxy":"","insecureHTTPParser":false,"authType":"","senderr":false,"headers":[],"x":610,"y":320,"wires":[["0d694ab3c96414a8","f99d32651f8ddfa5"]]},{"id":"0d694ab3c96414a8","type":"debug","z":"afdad340469dd9d3","name":"debug 3","active":true,"tosidebar":true,"console":false,"tostatus":false,"complete":"payload","targetType":"msg","statusVal":"","statusType":"auto","x":880,"y":400,"wires":[]},{"id":"f99d32651f8ddfa5","type":"api-call-service","z":"afdad340469dd9d3","name":"","server":"7874f07a.dd83f","version":5,"debugenabled":false,"domain":"browser_mod","service":"notification","areaId":[],"deviceId":[],"entityId":[],"data":"{\"message\":\"Matroparen skickad!\"}","dataType":"json","mergeContext":"","mustacheAltTags":false,"outputProperties":[],"queue":"first","x":890,"y":240,"wires":[[]]},{"id":"7874f07a.dd83f","type":"server","name":"Home Assistant","version":4,"addon":true,"rejectUnauthorizedCerts":true,"ha_boolean":"y|yes|true|on|home|open","connectionDelay":true,"cacheJson":true,"heartbeat":false,"heartbeatInterval":30,"areaSelector":"friendlyName","deviceSelector":"friendlyName","entitySelector":"friendlyName","statusSeparator":"at: ","statusYear":"hidden","statusMonth":"short","statusDay":"numeric","statusHourCycle":"h23","statusTimeFormat":"h:m"}]
&lt;&#47;details&gt;
</pre>
</details>


**Card:**
````
type: vertical-stack
card_mod: null
style: |
  :host {
    margin: 0px;
    }
cards:
  - type: entities
    title: Matroparen
    card_mod: null
    style: |
      ha-card {
        padding-bottom: 100px;
        }
    entities:
      - entity: input_select.matroparen_vem
      - entity: input_text.matroparen_text
  - show_name: true
    show_icon: false
    type: button
    tap_action:
      action: call-service
      service: nodered.trigger
      service_data:
        entity_id: switch.lovelace_button
    show_state: false
    icon: 'null'
    name: Skicka
    card_mod: null
    style: |
      :host {
        box-shadown: 0px;
      }
      ha-card {
        position: absolute;
        top: -95px;
        background: none;
        border-radius: 3px;
        margin-left: 70px;
        margin-right: 70px;
        border: 1px solid white;
        margin-bottom: -60px
        }

````


