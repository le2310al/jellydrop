<script setup lang="ts">
import { FilterMatchMode, FilterOperator } from '@primevue/core/api'
import { createClient } from '@supabase/supabase-js'
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'
import InputText from 'primevue/inputtext'
import { onMounted, ref } from 'vue'

const jellies = ref()
const selectedJellies = ref()
const availability = ref(new Set())
const filters = ref()

const supabase = createClient(
  'https://pvzqhffqixkoeyulawzc.supabase.co',
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB2enFoZmZxaXhrb2V5dWxhd3pjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ5MjY1NDMsImV4cCI6MjA2MDUwMjU0M30.LfxcCsI1AHZ-X3_n8CYNLgfu8Drmgh7zvxkcTtvSPoE',
)

async function getJellies() {
  const { data } = await supabase.from('jellies').select()
  jellies.value = data
  jellies.value.forEach(element =>
    availability.value.add(element.availability),
  )
}

function initFilters() {
  filters.value = {
    global: { value: null, matchMode: FilterMatchMode.CONTAINS },
    name: {
      operator: FilterOperator.AND,
      constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }],
    },
    availability: { value: null, matchMode: FilterMatchMode.IN },
  }
}
initFilters()

onMounted(() => {
  getJellies()
})
</script>

<template>
  <div class="card">
    <DataTable
      v-model:selection="selectedJellies"
      v-model:filters="filters"
      :value="jellies"
      sort-field="name"
      :sort-order="1"
      removable-sort
      table-style="min-width: 50rem"
      filter-display="menu"
      :global-filter-fields="['name', 'availability']"
      :virtual-scroller-options="{ itemSize: 100 }"
    >
      <template #header>
        <div class="flex justify-between">
          <Button
            type="button"
            icon="pi pi-filter-slash"
            label="Clear Filters"
            outlined
            @click="initFilters()"
          />
          <IconField>
            <InputIcon>
              <i class="pi pi-search" />
            </InputIcon>
            <InputText
              v-model="filters.global.value"
              placeholder="Keyword Search"
            />
          </IconField>
        </div>
      </template>
      <template #empty>
        No jellies found.
      </template>
      <Column selection-mode="multiple" header-style="width: 3rem" />
      <Column field="name" header="Name" sortable>
        <template #body="{ data }">
          {{ data.name }}
        </template>
        <template #filter="{ filterModel }">
          <InputText
            v-model="filterModel.value"
            type="text"
            placeholder="Search by name"
          />
        </template>
      </Column>
      <Column
        filter-field="availability"
        header="Availability"
        :show-filter-match-modes="false"
        sortable
      >
        <template #body="{ data }">
          <div class="flex items-center gap-2">
            <span>{{ data.availability }}</span>
          </div>
        </template>
        <template #filter="{ filterModel }">
          <MultiSelect
            v-model="filterModel.value"
            :options="Array.from(availability)"
            option-label="availability"
            placeholder="Any"
          >
            <template #option="slotProps">
              <div class="flex items-center gap-2">
                <span>{{ slotProps.option }}</span>
              </div>
            </template>
          </MultiSelect>
        </template>
      </Column>
    </DataTable>
  </div>
</template>
