<script setup>
import { zodResolver } from '@primevue/forms/resolvers/zod'
import { useToast } from 'primevue/usetoast'
import { ref, watch } from 'vue'
import { z } from 'zod'

const toast = useToast()
const selectedAction = ref('logOn')

const resolver = ref(zodResolver(
  z.object({
    email: z.string().min(1, { message: '' }),
  }),
))

function changeAction(action) {
  if (action === 'LogOn') {
    resolver.value = zodResolver(
      z.object({
        email: z.string().min(1, { message: '' }),
      }),
    )
  }
  else if (action === 'Sub') {
    resolver.value = zodResolver(
      z.object({
        email: z.string().min(1, { message: '' }),
      }),
    )
  }
  else if (action === 'UnSub') {
    resolver.value = zodResolver(
      z.object({
        email: z.string().min(1, { message: '' }),
      }),
    )
  }
}

watch(selectedAction, (newAction) => {
  changeAction(newAction)
})

function onFormSubmit({ valid }) {
  if (valid) {
    toast.add({ severity: 'success', summary: 'Form is submitted.', life: 3000 })
  }
}
</script>

<template>
  <div class="card flex flex-col items-center gap-5">
    <Toast />
    <Fieldset legend="Options">
      <RadioButtonGroup v-model="selectedAction" name="action" class="flex flex-wrap gap-4" @update:model-value="changeAction">
        <div class="flex items-center gap-2">
          <RadioButton input-id="logon" value="LogOn" />
          <label for="logon">Log On</label>
        </div>
        <div class="flex items-center gap-2">
          <RadioButton input-id="sub" value="Sub" />
          <label for="sub">Subscribe</label>
        </div>
        <div class="flex items-center gap-2">
          <RadioButton input-id="unsub" value="UnSub" />
          <label for="unsub">Unsubscribe</label>
        </div>
      </RadioButtonGroup>
    </Fieldset>

    <Form v-slot="$form" :initial-values :resolver="resolver" class="flex flex-col gap-4 w-full sm:w-56" @submit="onFormSubmit">
      <div class="flex flex-col gap-1">
        <InputText name="email" type="text" placeholder="Username" fluid />
        <Message v-if="$form.email?.invalid" severity="error" size="small" variant="simple">
          {{ $form.email.error.message }}
        </Message>
      </div>
      <Button type="submit" label="Submit" />
    </Form>
  </div>
</template>
