declare module 'zarr-gl' {
  export interface ZarrLayerOptions {
    id: string
    source: string
    variable: string
    colormap?: number[][]
    vmin?: number
    vmax?: number
    opacity?: number
    map?: any
  }
  export class ZarrLayer {
    constructor(options: ZarrLayerOptions)
  }
}
