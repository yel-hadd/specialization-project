"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";

// GET hook tracking loading/error state; pass null to skip the request.
export function useFetch<T>(path: string | null) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!path) return;
    let active = true;
    setLoading(true);
    api
      .get<T>(path)
      .then((d) => active && setData(d))
      .catch((e) => active && setError(String(e)))
      .finally(() => active && setLoading(false));
    return () => {
      active = false;
    };
  }, [path]);

  return { data, loading, error };
}
