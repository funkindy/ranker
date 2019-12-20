<template>
  <v-row dense class="mx-0" style="height: 100%">
    <v-navigation-drawer app :clipped="true" width="400" v-model="showSider">
      <v-list three-line>
        <template
          v-for="item in $store.state.event.list.content"
        >
          <v-list-item
            :key="item.title"
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
          <v-divider :key="item.title"/>
        </template>
      </v-list>
    </v-navigation-drawer>
    <v-col>
      <EventCard
        v-if="selectedId > 0"
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
      selectedId: -1, 
      showSider: true
    }
  },
  methods: {
    onEventClick(event_id) {
      this.$store.dispatch('fetchEventDetails', event_id)
      this.selectedId = event_id
    }
  },
  created() {
    this.$store.dispatch('fetchEvents')
  }
}
</script>
