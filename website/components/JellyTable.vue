<template>
  <div class="card">
    <DataTable
      v-model:selection="selectedJellies"
      v-model:filters="filters"
      :value="jellies"
      sortField="name"
      :sortOrder="1"
      removableSort
      tableStyle="min-width: 50rem"
      filterDisplay="menu"
      :globalFilterFields="['name', 'availability']"
      :virtualScrollerOptions="{ itemSize: 100 }"
    >
      <template #header>
        <div class="flex justify-between">
          <Button
            type="button"
            icon="pi pi-filter-slash"
            label="Clear"
            outlined
            @click="clearFilter()"
          />
          <IconField>
            <InputIcon>
              <i class="pi pi-search" />
            </InputIcon>
            <InputText
              v-model="filters['global'].value"
              placeholder="Keyword Search"
            />
          </IconField>
        </div>
      </template>
      <template #empty> No jellies found. </template>
      <Column selectionMode="multiple" headerStyle="width: 3rem"></Column>
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
        filterField="availability"
        header="Availability"
        :showFilterMatchModes="false"
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
            optionLabel="availability"
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

<script lang="ts">
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import { FilterMatchMode, FilterOperator } from "@primevue/core/api";
import { onMounted, ref } from "vue";
const jellies = ref();

async function getJellies() {
  const { data } = await supabase.from("jellies").select();
  jellies.value = data;
  jellies.value.forEach((element) =>
    console.log(availability.value.add(element.availability)),
  );
  console.log(selectedJellies);
}

const filters = ref();

const initFilters = () => {
  filters.value = {
    global: { value: null, matchMode: FilterMatchMode.CONTAINS },
    name: {
      operator: FilterOperator.AND,
      constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }],
    },
    availability: { value: null, matchMode: FilterMatchMode.IN },
  };
};
initFilters();
const clearFilter = () => {
  initFilters();
};
onMounted(() => {
  getJellies();
});

const availability = ref(new Set());
const selectedJellies = ref();
</script>