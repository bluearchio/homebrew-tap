class TagManager < Formula
  desc "AWS Tag Manager CLI - FinOps, compliance, and cost optimization tool"
  homepage "https://bluearch.io"
  version "v0.3.3"
  license :cannot_represent

  depends_on arch: :arm64

  url "https://dist.bluearch.io/tag-manager/v0.3.3/tag-manager_macos_arm64"
  sha256 "e9bc4f487d7d629791318be93ad5cd82a1de92c91b3f792a16829e1707624f6c"

  def install
    bin.install "tag-manager_macos_arm64" => "tag-manager"
  end

  test do
    system "#{bin}/tag-manager", "--version"
  end
end
