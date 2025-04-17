import { supabase } from "$lib/supabaseClient";

export async function load() {
  const { data } = await supabase.from("jellies").select();
  return {
    jellies: data ?? [],
  };
}
