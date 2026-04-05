import { useEffect } from 'react'
import { useSearchStore } from '../store/useSearchStore'

export function useSearch(){
  const query = useSearchStore(state => state.query)
  useEffect(()=>{
    // placeholder
  },[query])
}
