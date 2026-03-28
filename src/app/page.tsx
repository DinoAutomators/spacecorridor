import { HeroSection } from "@/components/landing/hero-section";
import { ProblemSection } from "@/components/landing/problem-section";
import { HowItWorksSection } from "@/components/landing/how-it-works-section";
import { Footer } from "@/components/layout/footer";

export default function Home() {
  return (
    <>
      <HeroSection />
      <ProblemSection />
      <HowItWorksSection />
      <Footer />
    </>
  );
}
