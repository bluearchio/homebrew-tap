class TagManager < Formula
  desc "AWS Tag Manager CLI - FinOps, compliance, and cost optimization tool"
  homepage "https://bluearch.io"
  version "0.0.0"
  license :cannot_represent

  on_macos do
    if Hardware::CPU.arm?
      url "https://dist.bluearch.io/tag-manager/latest/tag-manager_macos_arm64"
      sha256 "PLACEHOLDER_SHA256_ARM64"
    else
      url "https://dist.bluearch.io/tag-manager/latest/tag-manager_macos_x86_64"
      sha256 "PLACEHOLDER_SHA256_X86_64"
    end
  end

  def install
    if Hardware::CPU.arm?
      bin.install "tag-manager_macos_arm64" => "tag-manager"
    else
      bin.install "tag-manager_macos_x86_64" => "tag-manager"
    end
  end

  test do
    system "#{bin}/tag-manager", "--version"
  end
end
