import { useEffect, useRef } from 'react'
import { ZarrLayer } from 'zarr-gl'
import mapboxgl, { type CustomLayerInterface } from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'

mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_TOKEN as string

export default function App() {
  const containerRef = useRef<HTMLDivElement | null>(null)
  const mapRef = useRef<mapboxgl.Map | null>(null)

  useEffect(() => {
    if (mapRef.current || !containerRef.current) return

    const map = new mapboxgl.Map({
      container: containerRef.current,
      style: 'mapbox://styles/mapbox/streets-v12',
      center: [0, 0],
      zoom: 3,
      renderWorldCopies: true,
      antialias: true,
      projection: 'mercator',
    })

    const layer = new ZarrLayer({
      map,
      id: 'gradient-layer',
      source: './example.zarr',
      variable: 'my_array',
      // source: './gradient.zarr',
      // variable: 'precip',
      // @ts-expect-error: its needed to work
      version: 'v2',
      colormap: [
        [200, 10, 50],
        [30, 180, 140],
        [240, 220, 70],
      ],
      vmin: 0,
      vmax: 100,
      opacity: 0.7,
      invalidate: () => map.triggerRepaint(),
    })

    map.on('load', () => {
      map.addLayer(layer as CustomLayerInterface)
    })

    mapRef.current = map
    return () => {
      map.remove()
      mapRef.current = null
    }
  }, [])

  return <div ref={containerRef} style={{ height: '100vh', width: '100vw' }} />
}
