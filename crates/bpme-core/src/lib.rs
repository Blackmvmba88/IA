#[derive(Debug, Clone, Copy, PartialEq)]
pub struct SpurGear {
    pub teeth: u32,
    pub module_mm: f64,
}

impl SpurGear {
    pub fn pitch_diameter_mm(&self) -> Result<f64, &'static str> {
        if self.teeth < 6 {
            return Err("teeth must be >= 6");
        }
        if !self.module_mm.is_finite() || self.module_mm <= 0.0 {
            return Err("module_mm must be positive and finite");
        }
        Ok(self.teeth as f64 * self.module_mm)
    }
}

pub fn center_distance_mm(a: SpurGear, b: SpurGear) -> Result<f64, &'static str> {
    Ok((a.pitch_diameter_mm()? + b.pitch_diameter_mm()?) / 2.0)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn genesis_18_72_center_distance() {
        let a = SpurGear { teeth: 18, module_mm: 1.0 };
        let b = SpurGear { teeth: 72, module_mm: 1.0 };
        assert_eq!(center_distance_mm(a, b).unwrap(), 45.0);
    }
}
