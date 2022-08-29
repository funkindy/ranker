<template>
  <v-row dense class="mx-0" style="height: 100%">
    <v-navigation-drawer app :clipped="true" width="400" v-model="showSider">
      <v-card tile>
        <v-card-title>
          <div class="overline">{{ $t("events_list.name") }}</div>
        </v-card-title>
        <v-card-text class="px-0">
          <v-text-field
            class="mx-4" 
            v-model="eventSearch"
            append-icon="mdi-account-search-outline"
            :label="$t('events_list.search')"
            dense
            outlined
            single-line
            hide-details
          ></v-text-field>
          <v-list three-line>
            <v-list-item-group v-if="filteredEvents.length" color="primary">
              <v-divider />
              <template v-for="item in filteredEvents"  :key="item.id">
                <v-list-item
                 
                  @click="onEventClick(item.id)"
                >
                  <v-list-item-action class="my-auto">
                    <v-icon>mdi-bank</v-icon>
                  </v-list-item-action>

                  <v-list-item-content>
                    <v-list-item-title>
                      <b>{{ item.short_name }}</b>, {{ item.address }}
                    </v-list-item-title>
                    <v-list-item-subtitle>
                      {{ item.name }}
                    </v-list-item-subtitle>
                  </v-list-item-content>
                  <v-list-item-action>
                    <v-list-item-action-text>
                      {{ $t("event.coef") }}: {{ item.coefficient }}
                    </v-list-item-action-text>
                  </v-list-item-action>

                </v-list-item>
                <v-divider />
              </template>
            </v-list-item-group>
            <v-list-item class="text-center" v-else>
              <v-list-item-title>
                <v-icon>mdi-message-alert-outline</v-icon>
                {{ $t("events_list.not_found") }}
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-card-text>
      </v-card>
    </v-navigation-drawer>
    <v-col>
      <EventCard
        v-if="$store.state.event.list.selectedId > 0"
        :info="$store.state.event.details.info"
      />
      <v-card v-else>
        <v-card-title>
          <v-icon left>
            mdi-arrow-left-circle-outline
          </v-icon>
          <span>{{ $t("event_card.placeholder") }}</span>
        </v-card-title>
      </v-card>
    </v-col>
    <v-btn
      fab
      small
      fixed
      right
      bottom
      dark
      color="red"
      @click.stop="showSider = !showSider"
    > 
      <v-icon v-if="showSider">mdi-arrow-left</v-icon>
      <v-icon v-else>mdi-bank</v-icon>
    </v-btn>
  </v-row>
</template>
<script>
import EventCard from '@/components/EventCard'

export default {
  name: "events",
  components: { EventCard },
  data() {
    return {
      showSider: true,
      eventSearch: ""
    }
  },
  methods: {
    onEventClick(event_id) {
      this.$store.dispatch('fetchEventDetails', event_id)
      this.$store.commit('SET_SELECTED_EVENT_ID', event_id)
    }
  },
  computed: {
    filteredEvents() {
      var content = this.$store.state.event.list.content
      if (this.eventSearch) {
        content = content.filter((event) => {
          return event.name.toLowerCase().includes(this.eventSearch.toLowerCase())
        })
      }
      return content
    }
  },
  created() {
    this.$store.dispatch('fetchEvents')
  }
}
</script>
