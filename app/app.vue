<script setup>
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import { FilterMatchMode, FilterOperator } from "@primevue/core/api";
import { ref, onMounted } from "vue";
import { createClient } from "@supabase/supabase-js";
import InputText from "primevue/inputtext";

const supabase = createClient(
  "https://pvzqhffqixkoeyulawzc.supabase.co",
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB2enFoZmZxaXhrb2V5dWxhd3pjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ5MjY1NDMsImV4cCI6MjA2MDUwMjU0M30.LfxcCsI1AHZ-X3_n8CYNLgfu8Drmgh7zvxkcTtvSPoE",
);
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

import { zodResolver } from "@primevue/forms/resolvers/zod";
import { useToast } from "primevue/usetoast";
import { z } from "zod";

const toast = useToast();
const initialValues = ref({
  email: "",
});

const resolver = ref(
  zodResolver(
    z.object({
      email: z
        .string()
        .min(1, { message: "Email is required." })
        .email({ message: "Invalid email address." }),
    }),
  ),
);

const onFormSubmit = ({ valid }) => {
  if (valid) {
    toast.add({
      severity: "success",
      summary: "Form is submitted.",
      life: 3000,
    });
  }
};

const url = "https://api.onesignal.com/apps/app_id/users";
const options = {
  method: "POST",
  headers: { accept: "application/json", "content-type": "application/json" },
  body: JSON.stringify({
    identity: { external_id: "test_external_id" },
  }),
};

fetch(url, options)
  .then((res) => res.json())
  .then((json) => console.log(json))
  .catch((err) => console.error(err));
</script>

<template>
  <div class="card flex justify-center">
    <Form
      v-slot="$form"
      :resolver="resolver"
      :initialValues="initialValues"
      @submit="onFormSubmit"
      class="flex flex-col gap-4 w-full sm:w-56"
    >
      <div class="flex flex-col gap-1">
        <InputText name="email" type="text" placeholder="Email" fluid />
        <Message
          v-if="$form.email?.invalid"
          severity="error"
          size="small"
          variant="simple"
          >{{ $form.email.error?.message }}</Message
        >
      </div>
      <Button type="submit" severity="secondary" label="Submit" />
    </Form>
  </div>
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
      <Column field="name" header="Name" sortable="true">
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
        sortable="true"
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
