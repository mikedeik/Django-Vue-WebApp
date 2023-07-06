// src/types.ts

export interface PointOfInterest {
    id: number;
    name: string;
    description: string;
    longitude: number;
    latitude: number;
    categoryId: number[];
}
  